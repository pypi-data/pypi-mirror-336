# FastRTC

## The Real-Time Communication Library for Python

Turn any python function into a real-time audio and video stream over WebRTC or WebSockets. Now with the [Kroko-ASR TTS Model](https://huggingface.co/Banafo/Kroko-ASR)!

### Installation

```bash
pip install fastrtc-kroko
```

### Features

- Works with FastRTC with added support for the Kroko-ASR TTS model.
- Supports English and French Transcriptions (more will be added as Kroko is updated).

### Example Run

```python
import soundfile as sf
from pathlib import Path

curr_dir = Path(__file__).parent

from fastrtc_kroko import get_stt_model

m = get_stt_model() # You will need to set a HF_TOKEN env variable, or pass it in here.
audio, sr = sf.read(str(curr_dir / "test_file.wav"))
transcript = m.stt((sr, audio))
print(transcript)
```
### Documentation

Check out the [fastrtc documentation](https://fastrtc.org) for more information.

### Licence

MIT