from flask import Flask, send_file, request
import os
import pyttsx3
from google.cloud import texttospeech

app = Flask(__name__)


AUDIO_PATH = "output.wav"
JFK_PATH = "~/sample_data/JFK30.mp4"
NEIL_PATH = "~/sample_data/neil.mp4"
RESPONSE_PATH = "response.txt"


def generate_video(audio, baseline_person=""):
    os.system(
        f"python inference.py --checkpoint_path checkpoints/wav2lip_gan.pth --face {baseline_person} --audio {audio} --outfile result_voice.mp4"
    )


@app.route("/lipsync", methods=["GET"])
def lipsync():
    # Path to the file you want to send
    message = request.args["text"]
    """
    engine = pyttsx3.init()
    print(message)
    #engine.say(response["choices"][0]["text"])
    engine.save_to_file(message, 'output.wav')
    engine.runAndWait()

    """
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text="Hello, World!")

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
        name="en-US-Wavenet-B",
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
    if request.args["person"] == "jfk":
        baseline_person = JFK_PATH
    else:
        baseline_person = NEIL_PATH
    generate_video(AUDIO_PATH, baseline_person)
    file_path = "result_voice.mp4"
    # Send the file to the user
    print(file_path)
    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run()
