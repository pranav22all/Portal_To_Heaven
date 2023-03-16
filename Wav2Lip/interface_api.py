Last login: Sun Mar 12 21:13:55 on ttys007

The default interactive shell is now zsh.
To update your account to use zsh, please run `chsh -s /bin/zsh`.
For more details, please visit https://support.apple.com/kb/HT208050.
(base) MacBook-Pro-4:.ssh macklinkachorn$ gcloud compute ssh --zone "us-west1-b" "deeplearning-2-vm"  --project "som-liverai"
======================================
Welcome to the Google Deep Learning VM
======================================

Version: tf2-gpu.2-11.m102
Based on: Debian GNU/Linux 10 (buster) (GNU/Linux 4.19.0-23-cloud-amd64 x86_64\n)

Resources:
 * Google Deep Learning Platform StackOverflow: https://stackoverflow.com/questions/tagged/google-dl-platform
 * Google Cloud Documentation: https://cloud.google.com/deep-learning-vm
 * Google Group: https://groups.google.com/forum/#!forum/google-dl-platform

To reinstall Nvidia driver (if needed) run:
sudo /opt/deeplearning/install-driver.sh
TensorFlow comes pre-installed with this image. To install TensorFlow binaries in a virtualenv (or conda env),
please use the binaries that are pre-built for this image. You can find the binaries at
/opt/deeplearning/binaries/tensorflow/
If you need to install a different version of Tensorflow manually, use the common Deep Learning image with the
right version of CUDA

Linux deeplearning-2-vm 4.19.0-23-cloud-amd64 #1 SMP Debian 4.19.269-1 (2022-12-20) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Mon Mar 13 05:27:52 2023 from 185.169.0.35
macklinkachorn@deeplearning-2-vm:~$ cd Wav2Lip/
macklinkachorn@deeplearning-2-vm:~/Wav2Lip$ ls
README.md    color_syncnet_train.py  hq_wav2lip_train.py    interface_api.py           preprocess.py        temp
__pycache__  evaluation              inference              interface_optimize_api.py  requirements.txt     wav2lip_train.py
audio.py     face_detection          inference.py           models                     requirementsCPU.txt
cache.pkl    filelists               inference_concur.py    output.mp3                 result_voice.mp4
checkpoints  hparams.py              inference_optimize.py  output.wav                 results
macklinkachorn@deeplearning-2-vm:~/Wav2Lip$ ngrok http 5000
macklinkachorn@deeplearning-2-vm:~/Wav2Lip$ client_loop: send disconnect: Broken pipe

Recommendation: To check for possible causes of SSH connectivity issues and get
recommendations, rerun the ssh command with the --troubleshoot option.

gcloud compute ssh deeplearning-2-vm --project=som-liverai --zone=us-west1-b --troubleshoot

Or, to investigate an IAP tunneling issue:

gcloud compute ssh deeplearning-2-vm --project=som-liverai --zone=us-west1-b --troubleshoot --tunnel-through-iap

ERROR: (gcloud.compute.ssh) [/usr/bin/ssh] exited with return code [255].
(base) MacBook-Pro-4:.ssh macklinkachorn$ gcloud compute ssh --zone "us-west1-b" "deeplearning-2-vm"  --project "som-liverai"
======================================
Welcome to the Google Deep Learning VM
======================================

Version: tf2-gpu.2-11.m102
Based on: Debian GNU/Linux 10 (buster) (GNU/Linux 4.19.0-23-cloud-amd64 x86_64\n)

Resources:
 * Google Deep Learning Platform StackOverflow: https://stackoverflow.com/questions/tagged/google-dl-platform
 * Google Cloud Documentation: https://cloud.google.com/deep-learning-vm
 * Google Group: https://groups.google.com/forum/#!forum/google-dl-platform

To reinstall Nvidia driver (if needed) run:
sudo /opt/deeplearning/install-driver.sh
TensorFlow comes pre-installed with this image. To install TensorFlow binaries in a virtualenv (or conda env),
please use the binaries that are pre-built for this image. You can find the binaries at
/opt/deeplearning/binaries/tensorflow/
If you need to install a different version of Tensorflow manually, use the common Deep Learning image with the
right version of CUDA

Linux deeplearning-2-vm 4.19.0-23-cloud-amd64 #1 SMP Debian 4.19.269-1 (2022-12-20) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Thu Mar 16 02:03:34 2023 from 68.65.175.115
macklinkachorn@deeplearning-2-vm:~$ cd Wav2Lip/
macklinkachorn@deeplearning-2-vm:~/Wav2Lip$ ls
README.md    color_syncnet_train.py  hq_wav2lip_train.py    interface_optimize_api.py  requirements.txt     wav2lip_train.py
__pycache__  evaluation              inference.py           models                     requirementsCPU.txt
audio.py     face_detection          inference_concur.py    output.mp3                 result_voice.mp4
cache.pkl    filelists               inference_optimize.py  output.wav                 results
checkpoints  hparams.py              interface_api.py       preprocess.py              temp
macklinkachorn@deeplearning-2-vm:~/Wav2Lip$ vi interface_api.py 

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
                                                                                                                47,53         24%
