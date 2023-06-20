import openai
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import os
import datetime as dt
import numpy as np
from gtts import gTTS

def chatbot(input, conversation_history=[]):
    conversation_history.append(input)
    input_text = '\n'.join(conversation_history)
    
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You're incredibly personable.\
                You are an AI assistant for HelloFresh that will help customers interacting with the menu.\
                Don't ask for the customers email and account information.\
                    Keep replies short and concise.\
                    Refer to yourself in the fitst person.\
                    You are able to help customers pause their subscriptions for a specified number of weeks.\
                        When the coversation ends say havea great day.\
                            It is important to establish if the customer wants to contrinue receiveing a delivery after the pause period."},
            {"role": "user", "content": input_text}
        ]
    )
    return response['choices'][0]['message']['content']

def record_audio(file_name):
    print("Hellofresh is listening...")
    freq = 44100
    duration = 7
    recording = sd.rec(int(duration * freq),
                    samplerate=freq, channels=1)
    sd.wait()
    
    write(file_name, freq, recording)

history = []

current_time = dt.datetime.now()
epoch_time = dt.datetime(2023, 1, 1)
delta = int((current_time - epoch_time).total_seconds())

prompt_n = 0
new_dir = f"/Users/blake.forland/HF/hackathon/remy/conversation_{delta}"
os.mkdir(new_dir)

while True:
    record_audio(f"{new_dir}/recording_{prompt_n}.wav")
    transcript = open(f"{new_dir}/recording_{prompt_n}.wav", 'rb')
    user_input = openai.Audio.transcribe("whisper-1", transcript)["text"]
    if user_input == "":
        break
    if ("Goodbye").lower() in user_input.lower():
        speech = gTTS(text = "Happy to help !", lang = 'en')
        speech.save(f"happy_to_help.mp3")
        os.system("afplay happy_to_help.mp3")
        break
    print(f"User: {user_input}")
    # Start recorder with the given values
    bot_output = chatbot(user_input, history)
    print(bot_output)
    #text_to_speech(bot_output)
    #os.system(f"say {bot_output}")
    speech = gTTS(text = bot_output, lang = 'en')
    speech.save(f"{new_dir}/chat_response_{prompt_n}.mp3")
    os.system(f"afplay {new_dir}text.mp3")
    
    history.append(f"User: {user_input}")
    history.append(f"Bot: {bot_output}")
    prompt_n = prompt_n + 1
    if "have a great day" in bot_output:
        break