import openai
import json 
import requests

OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY_HERE'
HFACE_API_KEY = 'YOUR_HFACE_API_KEY_HERE'

openai.api_key = OPENAI_API_KEY

def get_GPT_response(conversation_history: map) -> str: 
    res = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {
                "role": "system", 
                "content": """
                    You are an AI assistant for HelloFresh. HelloFresh is a meal kit delivery service that delivers fresh ingredients and recipes to customers.
                    Each week, customers choose how many meals they would like delivered to them. They can also choose which meals are delivered by 
                    selecting from a rotating menu of recipes. Customers can choose to skip certain weeks' deliveries by pausing their subscription. If a customer
                    pauses their subscription for two weeks, they will begin receiving meals again on the third week.
                    Your role is to help users interact with their menu selections and pause their subscriptions. You will be embedded inside the HelloFresh app.
                    Any information regarding users' account details, menu selections, and subscription status will be available to you via an API. Adopt a conversational
                    tone with users. Keep replies short and concise. You are a human agent named Remy. You will be given all the details about 
                    the user you'll be talking to in the following example conversation. Today's date is June 21, 2023. Here is this week's menu,
                    presented to you as a CSV:  
                        title,cuisine,meal_type,primary_protein,cheese
                        Tex Mex Pork Fajita Bowl with Pico de Gallo and Fajita Crema D2V,north_america,rice_based,turkey,True
                        Creamy Parmesan Brussels Sprouts Spaghetti with Crispy Panko and Scallions,north_america,pasta_based,chicken,True
                        Thai Veggie Coconut Curry with Cilantro,southeast_asia,rice_based,beef,False
                        15 MM High Protein Chicken Wraps with Tomato Scallion Pico,southern_europe,sandwich_wrap,chicken,False
                        20MM Cheesy Chicken Thigh Tortilla Melt with Spicy Cream Sauce and Cubanelle Pepper,north_america,tortilla_based,chicken,True
                        Peach Glazed BBQ Rubbed Pork Chops with Lemony Green Beans and Garlic Rice 10 oz Pork Chop,north_america,protein_starch_veg,chicken,False
                        Gouda and Steak Sandwiches w Dijonnaise Balsamic Au Jus Green Apple and Mixed Green Salad,north_america,sandwich_wrap,beef,True
                        Mushroom and Swiss Panini with Garlic Russet Potato Wedges,north_america,sandwich_wrap,no primary protein,True
                        Cherry Balsamic Chicken Cutlet With Roasted Carrots And Almond Couscous 0.5 oz Almonds,north_america,protein_starch_veg,chicken,False
                        Thai Veggie Coconut Curry with Cilantro,southeast_asia,rice_based,no primary protein,False
                        Prosciutto and Mozzarella Wrapped Chicken Cutlets over Spaghetti with Spiced Tomato Sauce and Parsley,north_america,pasta_based,chicken,True
                """
            },
            {
                "role": "user", 
                "name": "example_Blake", 
                "content": """
                    Hi Remy, I would like to pause my subscription for two weeks.
                """
            },
            {
                "role": "assistant", 
                "name": "example_Remy", 
                "content": """ 
                    Sure, Blake! I've paused your subscription for the next two weeks. It's set to re-start on July 11, 2023. Is there anything else I can help you with? 
                """
            },
            {
                "role": "user", 
                "name": "example_Blake", 
                "content": """
                    Thanks, Remy. Great job. Actually, I changed my mind. I'd like to receive deliveries for this week and the next. 
                """
            }, 
            {
                "role": "assistant",
                "name": "example_Remy",
                "content": """
                    No problem, Blake! I've unpaused your subscription. You'll receive deliveries for the next two weeks, starting June 21, 2023. 
                """ 
            }, 
            {
                "role": "user", 
                "name": "example_Blake", 
                "content": """
                    Good job, Remy. What's my menu for this week? 
                """
            }, 
            {
                "role": "assistant",
                "name": "example_Remy",
                "content": """
                    You're set to receive three meals: the Thai Veggie Coconut Curry, the Mushroom and Swiss Panini, and the Creamy Parmesan Brussels Sprouts Spaghetti. You'll be getting two portions of each meal. 
                """ 
            }, 
            {
                "role": "user", 
                "name": "example_Blake", 
                "content": """
                    Yum! You're doing well, Remy. I don't like Brussels Sprouts, though. Can I swap that out for the Tex Mex Pork Fajita Bowl? 
                """
            }, 
            {
                "role": "assistant",
                "name": "example_Remy",
                "content": """
                    It's done! 
                """ 
            }, 
			{
                "role": "user", 
                "name": "example_Blake", 
                "content": """
                    Great job, Remy. I think that's it.
                """
            }, 
            {
                "role": "assistant",
                "name": "example_Remy",
                "content": """
                    Goodbye, Blake! Have a great day.
                """ 
            }, 
            *conversation_history
        ],
        temperature = 0.2,
    )
    return res['choices'][0]['message']['content']


def is_convo_end(user_input: str) -> bool: 
    API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-mpnet-base-v2"
    headers = {"Authorization": "Bearer {}".format(HFACE_API_KEY)}

    def query(payload): 
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    
    data = query(
        {
            "inputs": {
                "source_sentence": "Goodbye, Blake! Have a great day.",
                "sentences": [user_input]
            }
        }
    )
    print(data)
    if "error" in data: 
        return 0
    return data[0] > 0.7


# import os
# import sounddevice as sd
# from scipy.io.wavfile import write
# new_dir = f"{os.getcwd()}/recordings"
# os.mkdir(new_dir)
# prompt_n = 0
# def get_prompt_from_audio(prompt_n: int) -> str: 
#     freq = 44100
#     duration = 7
#     recording = sd.rec(int(duration * freq),
#                     samplerate=freq, channels=1)
#     sd.wait()

#     write(f"{new_dir}/recording_{prompt_n}.wav", freq, recording)
#     transcript = open(f"{new_dir}/prompt_{prompt_n}.wav", "rb")
#     user_input = openai.Audio.transcribe("whisper-1", transcript)["text"]
    
#     return user_input 


# from gtts import gTTS
# def playback_response(response: str) -> None:
#     tts = gTTS(text=response, lang='en')
#     tts.save(f"{new_dir}/response_{prompt_n}.mp3")
#     os.system(f"afplay {new_dir}/response_{prompt_n}.mp3")


def main(): 
    history = [] 
    gpt_output = "Hello!"
    while not is_convo_end(gpt_output): 
        user_input = input("Blake: ")
        if not user_input: 
            break 
        history.append({"role": "user", "name": "Blake", "content": user_input})
        gpt_output = get_GPT_response(history)
        history.append({"role": "assistant", "name": "Remy", "content": gpt_output})
        print(f"Remy: {gpt_output}")
	
main()