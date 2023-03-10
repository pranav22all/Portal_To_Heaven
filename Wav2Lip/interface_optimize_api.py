from flask import Flask, send_file,request
import os 
import pyttsx3
app = Flask(__name__)


AUDIO_PATH = "output.wav"
JFK_PATH = "~/sample_data/JFK30.mp4"
NEIL_PATH = "~/sample_data/neil.mp4"
RESPONSE_PATH = "response.txt"


@app.route('/lipsync',methods=["GET"])
def lipsync():
    # Path to the file you want to send
    message = request.args["text"]

    engine = pyttsx3.init()
    print(message)
    #engine.say(response["choices"][0]["text"])
    engine.save_to_file(message, 'output.wav')
    engine.runAndWait()
    if request.args["person"] == "jfk":
        baseline_person = JFK_PATH
    else:
        baseline_person = NEIL_PATH
    model = load_model("checkpoints/wav2lip_gan.pth")
    generate_video(AUDIO_PATH,baseline_person,model)
    file_path = "result_voice.mp4"
    # Send the file to the user
    print(file_path)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run()

