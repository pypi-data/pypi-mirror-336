import soundfile as sf
from pathlib import Path

curr_dir = Path(__file__).parent

from fastrtc_kroko import get_stt_model

m = get_stt_model()
audio, sr = sf.read(str(curr_dir / "test_file.wav"))
transcript = m.stt((sr, audio))
print(transcript)
