from sonusai.datatypes import AudioT
from sonusai.utils import ASRResult


def faster_whisper_validate(**config) -> None:
    model_name = config.get("model")
    if model_name is None:
        raise AttributeError("config must specify 'model'")


def faster_whisper(audio: AudioT, **config) -> ASRResult:
    from os import getpid
    from timeit import default_timer as timer

    from faster_whisper import WhisperModel

    model_name = config.get("model")
    if model_name is None:
        raise AttributeError("config must specify 'model'")

    device = config.get("device", "cpu")
    cpu_threads = config.get("cpu_threads", 1)
    compute_type = config.get("compute_type", "int8")
    beam_size = config.get("beam_size", 5)

    pid = getpid()
    # print(f'{pid}: Loading model ...')
    retry = 2
    count = 0
    while True:
        try:
            model = WhisperModel(model_name, device=device, cpu_threads=cpu_threads, compute_type=compute_type)

            # print(f'{pid}: Done Loading, now transcribing ...')
            s_time = timer()
            segments, info = model.transcribe(audio, beam_size=int(beam_size))
            # The transcription will actually run here (segments is an iterable).
            segments = list(segments)
            e_time = timer()
            elapsed = e_time - s_time
            transcription = "".join(segment.text for segment in segments)
            # print(f'{pid}: Done transcribing.')
            return ASRResult(
                text=transcription,
                lang=info.language,
                lang_prob=info.language_probability,
                duration=info.duration,
                num_segments=len(segments),
                asr_cpu_time=elapsed,
            )
        except Exception as e:
            count += 1
            print(f"{pid}: Warning: faster_whisper exception: {e}")
            if count >= retry:
                raise SystemError(f"{pid}: faster_whisper exception: {e.args}") from e


"""
Whisper results:
{
  'text': ' The birch canoe slid on the smooth planks.',
  'segments': [
    {
      'id': 0,
      'seek': 0,
      'start': 0.0,
      'end': 2.4,
      'text': ' The birch canoe slid on the smooth planks.',
      'tokens': [
        50363,
        383,
        35122,
        354,
        47434,
        27803,
        319,
        262,
        7209,
        1410,
        591,
        13,
        50483
      ],
      'temperature': 0.0,
      'avg_logprob': -0.4188103675842285,
      'compression_ratio': 0.8571428571428571,
      'no_speech_prob': 0.003438911633566022
    }
  ],
  'language': 'en'
}
"""
