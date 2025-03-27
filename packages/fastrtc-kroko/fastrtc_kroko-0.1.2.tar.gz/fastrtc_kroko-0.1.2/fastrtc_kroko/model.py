import os
from functools import lru_cache
from pathlib import Path
from typing import Literal, Protocol

import click
from dotenv import load_dotenv
import librosa
import numpy as np
import sherpa_onnx
import soundfile as sf
import torch
from huggingface_hub import hf_hub_download
from numpy.typing import NDArray

curr_dir = Path(__file__).parent
load_dotenv()

class STTModel(Protocol):
    def stt(self, audio: tuple[int, NDArray[np.int16 | np.float32]]) -> str: ...

@lru_cache
def get_stt_model(hf_token: str | None = None, lang: Literal["en", "fr"] = "en") -> STTModel:
    """
    Create an instance of the Kroko-ASR STT model.
    :param hf_token:
    :param lang:
    :return:
    """
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    m = KrokoSTT(hf_token=hf_token, lang=lang)

    try:
        print(click.style("INFO", fg="green") + ":\t Warming up Kroko-ASR STT model")
        audio, sr = sf.read(str(curr_dir / "test_file.wav"))
        m.stt((sr, audio))
        print(click.style("INFO", fg="green") + ":\t model warmed up!")

    except Exception as e:
        print(click.style("Warn", fg="red") + ":\t Could not warm up Kroko-ASR STT model.", e)

    return m

class KrokoSTT(STTModel):
    """
    Speech-to-text (STT) model using Kroko-ASR.

    :param hf_token: hugging face token to download gated models.
    :param lang: language to perform speech recognition. Currently supports english and french.
    """
    def __init__(self, hf_token: str | None = None, lang: Literal["en", "fr"] = "en"):
        self.lang = lang
        if not hf_token:
            self.hf_token = os.environ.get("HF_TOKEN")
            if not self.hf_token:
                raise ValueError("HF_TOKEN environment variable not set or provided")
        else:
            self.hf_token = hf_token

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_filenames = {
            "encoder": f"{self.lang}_encoder.onnx",
            "decoder": f"{self.lang}_decoder.onnx",
            "joiner": f"{self.lang}_joiner.onnx",
            "tokens": f"{self.lang}_tokens.txt",
        }
        self.model_paths = {}
        self._download_models()
        self.recognizer = self._create_recognizer()
        self.stream = self.recognizer.create_stream()

    def _download_models(self):
        """
        Downloads encoder, decoder, joiner and tokens.txt from huggingface.
        """
        repo_id = "Banafo/kroko-asr"
        for model_name, filename in self.model_filenames.items():
            self.model_paths[model_name] = hf_hub_download(repo_id=repo_id, token=self.hf_token, filename=filename)

    def _create_recognizer(self) -> sherpa_onnx.OnlineRecognizer:
        """
        Creates a recognizer using the downloaded models.
        """
        recognizer = sherpa_onnx.OnlineRecognizer.from_transducer (
            tokens=self.model_paths["tokens"],
            encoder=self.model_paths["encoder"],
            decoder=self.model_paths["decoder"],
            joiner=self.model_paths["joiner"],
            provider=self.device
        )

        return recognizer


    def stt(self, audio: tuple[int, NDArray[np.int16 | np.float32]]) -> str:
        sr, audio_np = audio # type: ignore
        if audio_np.dtype == np.int16:
            audio_np = audio_np.astype(np.float32) / 32768.0
        if sr != 16000:
            audio_np: NDArray[np.float32] = librosa.resample(audio_np, orig_sr=sr, target_sr=16000)
        if audio_np.ndim != 1:
            audio_np = audio_np.reshape(-1)


        pad_duration = 1
        pad_samples = int(pad_duration * 16000)
        pad_start = np.zeros(pad_samples, dtype=np.float32)
        pad_end = np.zeros(pad_samples, dtype=np.float32)
        audio_np = np.concatenate([pad_start, audio_np, pad_end])

        total_samples = audio_np.shape[0]
        chunk_size = 4000
        offset = 0

        while offset < total_samples:
            end = offset + chunk_size
            chunk = audio_np[offset:end]
            self.stream.accept_waveform(16000, chunk)
            while self.recognizer.is_ready(self.stream):
                self.recognizer.decode_stream(self.stream)
            offset += chunk_size

        result = self.recognizer.get_result(self.stream)
        self.recognizer.reset(self.stream)
        return result