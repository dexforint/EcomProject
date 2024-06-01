from faster_whisper import WhisperModel

model_size = "large-v3"

# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda", compute_type="float16")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")


def speech2text(audio_path):

    segments, info = model.transcribe(audio_path, beam_size=5, language="ru")

    text = []
    for segment in segments:
        text.append(segment.text)
        # print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

    text = " ".join(text).strip()
    return text
