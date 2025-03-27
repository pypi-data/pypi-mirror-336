from fastrtc_kroko import get_stt_model
from fastrtc import ReplyOnPause, Stream, AdditionalOutputs # You must install fastrtc for this example!
import gradio as gr

model = get_stt_model()

def echo(audio):
    text = model.stt(audio)
    yield AdditionalOutputs(text)

stream = Stream(ReplyOnPause(echo), mode="send-receive", modality="audio",
                additional_outputs=[gr.Textbox(label="Transcription")],
                additional_outputs_handler=lambda old,new:old + new)

stream.ui.launch()