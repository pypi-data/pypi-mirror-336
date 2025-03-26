from sonusai.datatypes import AudioT
from sonusai.utils import ASRResult


def google_validate(**_config) -> None:
    from os import getenv

    key = getenv("GOOGLE_SPEECH_API_KEY")
    if key is None:
        raise OSError("GOOGLE_SPEECH_API_KEY environment variable does not exist")


def google(audio: AudioT, **_config) -> ASRResult:
    import tempfile
    from os import getenv
    from os.path import getsize
    from os.path import join
    from random import random
    from time import sleep

    import speech_recognition as sr
    from sonusai.utils import ASRResult
    from sonusai.utils import float_to_int16
    from sonusai.utils import human_readable_size
    from sonusai.utils import write_audio

    key = getenv("GOOGLE_SPEECH_API_KEY")
    if key is None:
        raise OSError("GOOGLE_SPEECH_API_KEY environment variable does not exist")

    r = sr.Recognizer()
    with tempfile.TemporaryDirectory() as tmp:
        file = join(tmp, "asr.wav")
        write_audio(name=file, audio=float_to_int16(audio))
        size = getsize(file)
        if size > 10 * 1024 * 1024:
            print(f"Warning: file size exceeds Google single request limit: {human_readable_size(size)} > 10 MB")

        with sr.AudioFile(file) as source:
            audio = r.record(source)

        try:
            retry = 5
            count = 0
            while True:
                try:
                    sleep(count * (1 + random()))  # noqa: S311
                    results = r.recognize_google(audio, key=key, show_all=True)
                    if not isinstance(results, dict) or len(results.get("alternative", [])) == 0:
                        raise ValueError  # noqa: TRY301
                    break
                except ValueError:
                    print(f"Warning: speech_recognition ValueError {count}\n{results}")
                    count += 1
                    if count >= retry:
                        raise ValueError("speech_recognition exception: ValueError retry count exceeded.") from None

            if "confidence" in results["alternative"]:
                # return alternative with highest confidence score
                best_hypothesis = max(results["alternative"], key=lambda alternative: alternative["confidence"])
            else:
                # when there is no confidence available, we arbitrarily choose the first hypothesis.
                best_hypothesis = results["alternative"][0]
            if "transcript" not in best_hypothesis:
                raise ValueError("speech_recognition: UnknownValueError")
            confidence = best_hypothesis.get("confidence", 0.5)
            return ASRResult(text=best_hypothesis["transcript"], confidence=confidence)
        except sr.UnknownValueError:
            return ASRResult(text="", confidence=0)
        except sr.RequestError as e:
            raise SystemError(f"Could not request results from Google Speech Recognition service: {e}") from e


"""
Google results:
{
  "result": [
    {
      "alternative": [
        {
          "transcript": "the Birch canoe slid on the smooth planks",
          "confidence": 0.94228178
        },
        {
          "transcript": "the Burj canoe slid on the smooth planks"
        },
        {
          "transcript": "the Birch canoe slid on the smooth plank"
        },
        {
          "transcript": "the Birch canoe slit on the smooth planks"
        },
        {
          "transcript": "the Birch canoes slid on the smooth planks"
        }
      ],
      "final": true
    }
  ],
  "result_index": 0
}
"""
