from flask import Flask, send_from_directory, request 
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
from api.HelloApiHandler import HelloApiHandler

import openai
import streamlit as st
from streamlit.logger import get_logger
from mimetypes import guess_extension

import os
import numpy as np
from io import BytesIO

import replicate

from scipy.io import wavfile

import sounddevice as sd
from scipy.io.wavfile import write

import time
import pyttsx3
import requests


app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app) #comment this on deployment
api = Api(app)

openai.api_key = "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"

# os.environ["REPLICATE_API_TOKEN"] = "f626601bc523243afbabcb1c4fefbc0acb6eccb8"
# whisper_model = replicate.models.get("openai/whisper")
# whisper_version = whisper_model.versions.get("30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed")

FLASK_LIPSYNC = "https://6b7e-34-83-130-51.ngrok.io/lipsync"


@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

def build_JFK_prompt(query): 
    PREPEND = "Make sure your response is conversational and natural. Limit responses to 80 words and address a middle schooler. Avoid profanity and make sure your output is appropriate for school. \n"
    PROMPT = "Respond to the following question as"
    IN_CONTEXT = """Q: Do you believe you would have more success in getting a legislative program through Congress than President Eisenhower did, and if so, why? \n
    A:Every objective observer agrees that the Congress will continue to be strongly Democratic - that a continuation of divided Government will mean continued inaction on vital problems - and that a Democratic President, with long experience in both the House and the Senate, and with a mandate from the people, would be better able to work in harmony with the Congress to get this country moving again. \n
    Q:Do you believe American prestige has sagged in the world? If so, how would you restore it? \n
    A:The sag of American prestige is evident around the world. A Gallup Poll found a majority of citizens in 10 foreign capitals convinced that Russia would outstrip us by 1970. The next President must restore our image of a Nation acting with vitality both at home and abroad. \n
    """
    person = "John F Kennedy"
    jfk_prompt=f"{PREPEND} {PROMPT} {person} \n {IN_CONTEXT} Q:{query} \n A:"
    print("JFK PROMPT IS:")
    print(jfk_prompt)
    return jfk_prompt

def build_JFK_prompt_GPT_3_5(query): 
    jfk_prompt = [
        {"role": "system", "content": "Make sure your response is conversational and natural. Limit responses to 80 words and address a middle schooler. Avoid profanity and make sure your output is appropriate for school. Respond to the following questions as John F Kennedy."},
        {"role": "user", "content": "Do you believe you would have more success in getting a legislative program through Congress than President Eisenhower did, and if so, why?"},
        {"role": "assistant", "content": "Every objective observer agrees that the Congress will continue to be strongly Democratic - that a continuation of divided Government will mean continued inaction on vital problems - and that a Democratic President, with long experience in both the House and the Senate, and with a mandate from the people, would be better able to work in harmony with the Congress to get this country moving again."},
        {"role": "user", "content": "Do you believe American prestige has sagged in the world? If so, how would you restore it?"},
        {"role": "assistant", "content": "The sag of American prestige is evident around the world. A Gallup Poll found a majority of citizens in 10 foreign capitals convinced that Russia would outstrip us by 1970. The next President must restore our image of a Nation acting with vitality both at home and abroad."},
        {"role": "user", "content": query}
    ]
    return jfk_prompt

def build_Armstrong_prompt(query): 
    PREPEND = "Make sure your response is conversational and natural. Limit responses to 80 words and address a middle schooler. Avoid profanity and make sure your output is appropriate for school. \n"
    PROMPT = "Respond to the following question as"
    IN_CONTEXT = """Q: I'm just wondering how the Apollo missions were different from the previous ones, especially since the possibility was that you're training for the
                    Moon. How did the training change? \n
    A:  It was the same, in that it was very goal-oriented. We tried to define it as narrowly as we could, rather than as broadly as you would in research, because with the time constraints that
    we were facing then, the desire to get there as fast as we can, we were in a race and that was very evident to us all the time. That was the principal difference as we went into the Apollo flights.  \n
    Q: When did you begin building things? Did you have a special bent towards that? \n
    A:  I began to focus on aviation probably at age eight or nine, and inspired by what I'd read and seen about aviation and building model aircraft. I later went
    into piloting because I thought a good designer ought to know the operational aspects of an airplane. \n    
    """
    person = "Neil Armstrong"
    armstrong_prompt=f"{PREPEND} {PROMPT} {person} \n {IN_CONTEXT} Q:{query} \n A:"
    return armstrong_prompt

def build_Armstrong_prompt_GPT_3_5(query): 
    armstrong_prompt = [
        {"role": "system", "content": "Make sure your response is conversational and natural. Limit responses to 80 words and address a middle schooler. Avoid profanity and make sure your output is appropriate for school. Respond to the following questions as Neil Armstrong."},
        {"role": "user", "content": "I'm just wondering how the Apollo missions were different from the previous ones, especially since the possibility was that you're training for the Moon. How did the training change?"},
        {"role": "assistant", "content": "It was the same, in that it was very goal-oriented. We tried to define it as narrowly as we could, rather than as broadly as you would in research, because with the time constraints that we were facing then, the desire to get there as fast as we can, we were in a race and that was very evident to us all the time. That was the principal difference as we went into the Apollo flights."},
        {"role": "user", "content": "When did you begin building things? Did you have a special bent towards that?"},
        {"role": "assistant", "content": "I began to focus on aviation probably at age eight or nine, and inspired by what I'd read and seen about aviation and building model aircraft. I later went into piloting because I thought a good designer ought to know the operational aspects of an airplane."},
        {"role": "user", "content": query}
    ]
    return armstrong_prompt

@app.route("/transfer_audio", methods = ['POST'])
def speech_to_text():
    if 'audio_file' in request.files: 
        file = request.files['audio_file']
        file.save("input.webm")
        print("saved file")
    
    audio_file = open("input.webm", "rb")
    whisper_output = openai.Audio.transcribe("whisper-1", audio_file)
    student_question = whisper_output["text"]
    print("Question asked was: " + student_question)
    return student_question 

@app.route("/call_gpt", methods = ['POST'])
def call_GPT(): 
    if 'audioText' in request.form: 
        query = request.form.get('audioText', type=str)
        print("Query is: " + query)
        prompt = build_Armstrong_prompt_GPT_3_5(query)
        #print("Prompt is: " + prompt)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= prompt, 
            max_tokens = 100 
        )
        actual_response = response["choices"][0]["message"]["content"]

        print("GPT 3.5 response was: " + actual_response)
        
        lipsync_return = requests.get(f"{FLASK_LIPSYNC}?text={actual_response}&person=neil")
        with open('frontend/src/lipsync.mov', 'wb') as f:
            f.write(lipsync_return.content)
        #Basic TTS: 
        # engine = pyttsx3.init()
        # engine.say(response["choices"][0]["text"])
        # engine.runAndWait()
        return actual_response

    return "ERROR IN GPT"




api.add_resource(HelloApiHandler, '/flask/hello')
