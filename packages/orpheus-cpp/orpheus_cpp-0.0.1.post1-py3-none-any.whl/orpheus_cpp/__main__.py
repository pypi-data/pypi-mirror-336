import importlib.util

if importlib.util.find_spec("fastrtc") is None:
    raise RuntimeError(
        "fastrtc is not installed. Please install it using 'pip install fastrtc>=0.0.17'."
    )

import asyncio
import random

import gradio as gr
import httpx
import numpy as np
import numpy.typing as npt
from fastrtc import (
    AdditionalOutputs,
    AsyncStreamHandler,
    AudioEmitType,
    Stream,
    wait_for_item,
)
from fastrtc.utils import create_message
from huggingface_hub import InferenceClient

from orpheus_cpp.model import OrpheusCpp

async_client = httpx.AsyncClient()

client = InferenceClient(model="meta-llama/Llama-3.2-3B-Instruct")


def generate_message():
    system_prompt = """You are a creative text generator that generates short sentences from everyday life.
Example: "Hello!  I'm so excited to talk to you! This is going to be fun!"
Example: I'm nervous about the interview tomorrow
"""

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Give me a short sentence please."},
        ],
        max_tokens=100,
        seed=random.randint(0, 1000000),
    )
    msg = response.choices[0].message.content
    if msg:
        msg = msg.replace('"', "")
    return msg


model = OrpheusCpp()


class OrpheusStream(AsyncStreamHandler):
    def __init__(self):
        super().__init__(output_sample_rate=24_000, output_frame_size=480)
        self.latest_msg = ""
        self.latest_voice_id = "tara"
        self.audio_queue: asyncio.Queue[AudioEmitType] = asyncio.Queue()

    async def start_up(self):
        await self.wait_for_args()

    async def receive(self, frame: tuple[int, npt.NDArray[np.int16]]) -> None:
        msg, cb, voice_id, _ = self.latest_args[1:]
        if msg != self.latest_msg or voice_id != self.latest_voice_id:
            await self.send_message(create_message("log", "pause_detected"))

            # Initialize variables
            all_audio = np.array([], dtype=np.int16)
            started_playback = False

            async for sample_rate, chunk in model.stream_tts(
                msg, options={"voice_id": voice_id}
            ):
                all_audio = np.concatenate([all_audio, chunk.squeeze()])
                if not started_playback:
                    started_playback = True
                    await self.send_message(create_message("log", "response_starting"))
                await self.audio_queue.put((sample_rate, chunk))

            cb.append({"role": "user", "content": msg})
            cb.append(
                {
                    "role": "assistant",
                    "content": gr.Audio(value=(sample_rate, all_audio)),
                }
            )
            await self.audio_queue.put(AdditionalOutputs(cb))
            self.latest_msg = msg
            self.latest_voice_id = voice_id

    async def emit(self) -> AudioEmitType:
        return await wait_for_item(self.audio_queue)

    def copy(self):
        return OrpheusStream()


chat = gr.Chatbot(
    label="Conversation",
    type="messages",
    allow_tags=[
        "giggle",
        "laugh",
        "chuckle",
        "sigh",
        "cough",
        "sniffle",
        "groan",
        "yawn",
        "gasp",
    ],
)
generate = gr.Button(
    value="Generate Prompt",
)
AVAILABLE_VOICES = ["tara", "leah", "jess", "leo", "dan", "mia", "zac", "zoe"]
prompt = gr.Textbox(label="Prompt", value="Hello, how are you?")
stream = Stream(
    OrpheusStream(),
    modality="audio",
    mode="send-receive",
    additional_inputs=[
        prompt,
        chat,
        gr.Dropdown(choices=AVAILABLE_VOICES, value="tara", label="Voice"),
        generate,
    ],
    additional_outputs=[chat],
    additional_outputs_handler=lambda old, new: new,
    ui_args={
        "title": "Orpheus.cpp - Fast Streaming TTS over WebRTC",
        "subtitle": "Powered by FastRTC ⚡️ + llama.cpp 🦙",
        "send_input_on": "submit",
    },
)
with stream.ui:
    generate.click(generate_message, inputs=[], outputs=[prompt])


stream.ui.launch()
