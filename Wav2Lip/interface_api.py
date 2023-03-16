from flask import Flask, send_file, request
import os
import pyttsx3
from google.cloud import texttospeech

app = Flask(__name__)


AUDIO_PATH = "output.wav"
JFK_PATH = "~/sample_data/JFK30.mp4"
NEIL_PATH = "~/sample_data/neil.mp4"
NELSON_PATH = "~/sample_data/nelson.mp4"
ELEANOR_PATH = "~/sample_data/eleanor.mp4"
RICHARD_PATH = "~/sample_data/feyman.mp4"

RESPONSE_PATH = "response.txt"

def generate_video(audio, baseline_person="", resize_factor=1):
    os.system(
        f"python inference.py --checkpoint_path checkpoints/wav2lip_gan.pth --face {baseline_person} --audio {audio}  --resize_factor {resize_factor} --static True --outfile result_voice.mp4"
    )


@app.route("/lipsync", methods=["GET"])
def lipsync():
    # Path to the file you want to send
    message = request.args["text"]

    if request.args["person"] == "jfk":
        AUDIO_PATH = tts(message,"en-US-Standard-B",texttospeech.SsmlVoiceGender.MALE)
        baseline_person = JFK_PATH
    elif request.args["person"] == "neil" :
        AUDIO_PATH = tts(message,"en-US-Standard-B", texttospeech.SsmlVoiceGender.MALE)
        baseline_person = NEIL_PATH
    elif request.args["person"] == "mandela" :
        AUDIO_PATH = tts(message,"en-AU-News-G", texttospeech.SsmlVoiceGender.MALE)
        baseline_person = NELSON_PATH
    elif request.args["person"] == "roosevelt" :
        AUDIO_PATH =tts(message,"en-US-Standard-E", texttospeech.SsmlVoiceGender.FEMALE)
        baseline_person = ELEANOR_PATH
    elif request.args["person"] == "feynman" :
        AUDIO_PATH = tts(message,"en-US-Standard-J", texttospeech.SsmlVoiceGender.MALE)
        baseline_person = RICHARD_PATH
    else: 
        raise NotImplementedError("voice not in the library")
    if request.args["person"] == "mandela" or request.args["person"] == "feynman" :
        generate_video(AUDIO_PATH, baseline_person,2)
    else:
        generate_video(AUDIO_PATH, baseline_person)
    file_path = "result_voice.mp4"
    # Send the file to the user
    print(file_path)
    return send_file(file_path, as_attachment=True)


def tts(message,name,gender):
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=message)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=gender, 
        name=name,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open("output.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
        AUDIO_PATH = "output.mp3"
    return AUDIO_PATH

if __name__ == "__main__":
    app.run()
