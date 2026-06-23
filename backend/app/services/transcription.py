import asyncio
from faster_whisper import WhisperModel
from app.core.config import settings

print(
    f"Loading faster-whisper '{settings.WHISPER_MODEL}' model..."
)

# ប្តូរពី "medium" ទៅ "tiny" និងពី "cuda" ទៅ "cpu"
model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)

def process_audio_sync(file_path: str) -> str:
    segments, info = model.transcribe(
        file_path,
        beam_size=5,
        temperature=0.0,
        vad_filter=True,
        vad_parameters={
            "min_silence_duration_ms": 500
        },
        # មិនដាក់ language ទេ ដើម្បីឱ្យវា Auto-Detect គ្រប់ភាសា
        # ប៉ុន្តែយើងផ្តល់ការណែនាំចម្រុះភាសា ដើម្បីកុំឱ្យវាលម្អៀងទៅរកតែសំឡេងហ្គេមអង់គ្លេស
        initial_prompt="សួស្តី Hello 你好 Здравствуйте" 
    )

    print(
        f"Detected language: {info.language} "
        f"(Probability: {info.language_probability:.2f})"
    )

    texts = []

    for segment in segments:
        if hasattr(segment, "no_speech_prob"):
            if segment.no_speech_prob > 0.5:
                continue

        texts.append(segment.text.strip())

    final_text = " ".join(texts).strip()

    if len(final_text) < 2:
        return "No speech detected"

    return final_text


async def transcribe_audio(file_path: str) -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None,
        process_audio_sync,
        file_path
    )