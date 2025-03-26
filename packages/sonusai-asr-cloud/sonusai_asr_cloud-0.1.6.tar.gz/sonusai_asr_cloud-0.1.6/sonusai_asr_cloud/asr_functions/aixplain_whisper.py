from sonusai.datatypes import AudioT
from sonusai.utils import ASRResult


def aixplain_whisper_validate(**config) -> None:
    from os import getenv

    model_name = config.get("model")
    if model_name is None:
        raise AttributeError("config must specify 'model'")

    env_var = "AIXP_WHISPER_" + model_name.upper()
    model_key = getenv(env_var)
    if model_key is None:
        raise OSError(f"{env_var} environment variable does not exist")


def aixplain_whisper(audio: AudioT, **config) -> ASRResult:
    import tempfile
    from os import getenv
    from os.path import join

    from aixplain.factories.model_factory import ModelFactory
    from sonusai.utils import ASRResult
    from sonusai.utils import float_to_int16
    from sonusai.utils import write_audio

    model_name: str | None = config.get("model")
    if model_name is None:
        raise AttributeError("config must specify 'model'")

    env_var = "AIXP_WHISPER_" + model_name.upper()
    model_key = getenv(env_var)
    if model_key is None:
        raise OSError(f"{env_var} environment variable does not exist")

    model = ModelFactory.get(model_key)

    with tempfile.TemporaryDirectory() as tmp:
        file = join(tmp, "asr.wav")
        write_audio(name=file, audio=float_to_int16(audio))

        retry = 5
        count = 0
        while True:
            try:
                results = model.run(file)
                return ASRResult(text=results["data"], confidence=results["confidence"])
            except Exception as e:
                count += 1
                print(f"Warning: aiXplain exception: {e}")
                if count >= retry:
                    raise SystemError(f"Whisper exception: {e.args}") from e


"""
aiXplain Whisper results:
{
  'completed': True,
  'data': 'The birch canoe slid on the smooth planks.',
  'usedCredits': 3.194770833333333e-05,
  'runTime': 114.029,
  'confidence': None,
  'details': [],
  'rawData': {
    'predictions': [
      ' The birch canoe slid on the smooth planks.'
    ]
  },
  'status': 'SUCCESS'
}
"""
