from fastrtc_kroko import get_stt_model
from fastrtc import ReplyOnPause, Stream # You must install fastrtc for this example!

model = get_stt_model()

def echo(audio):
    text = model.stt(audio)
    print(text)
    yield audio


stream = Stream(ReplyOnPause(echo), modality='audio', mode='send-receive')
stream.ui.launch()