def clear(): print ('\033[J\033[K')
clear()

import pandas as pd
import numpy as np

import openai
import time
menu=pd.read_csv('sample_upcoming_data.csv')
menu['title_split']=menu['title'].\
    apply(lambda s:s.replace('[','/').replace(']','/').split('/'))
menu['title_len']=menu['title_split'].apply(len)
# menu=menu.query('title_len==3')
# menu['title']=menu['title_split'].apply(lambda l:l[1].lower())
# menu['description']=menu['title_split'].apply(lambda l:l[2].lower())
# menu=menu.drop(['title_split','title_len'],axis=1)
# menu=menu.iloc[:10]

openai.api_key = 'YOUR_OPENAI_API_KEY_HERE'

def chatbot(conversation_history):
    
    mess_content="""
    You're incredibly personable.
    You are an AI assistant for HelloFresh that will help customers interacting with the menu.
    Don't ask for the customers email and account information.
    Keep replies short and concise.
    Refer to yourself in the first person.
    When the conversation ends say "have a great day".
    It is important to establish if the customer wants to continue receiving a delivery after the pause period.
    """
    mess_content+='You are also abot to make recommendation for HelloFresh meal.'
    mess_content+='It is important to keep in mind, you can only make the suggestion from the following meals:'
    
    for title in list(menu['title'].unique())[:2]:
        mess_content+=title+','
        
    
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": mess_content},
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
        ]
    )
    return response['choices'][0]['message']['content']

history = []
u_input=['Hello there, could you help me with hellofresh menu?',\
          'Yes. Could you recommend some hellofresh menu to me?',
         
#           # 'Got it. Many thanks. They all sound tasty. I will pick the Creamy Dill Chicken. I will cook a dinner for a friend from Boston. Any thing special for him?',
          
#           # 'I see. Any lobster in HelloFresh menu?',
          
#           # 'Got it. Let us do Spaghetti and Lemon Herb Scallops.Any vegetarian option?',
          
#           # 'Got it. I will go for Sweet Potato and Black Bean Tacos. Can you summarize my choice.',
          
#           # 'That is. Many thanks.'
           ]
    
b_output=[]
for i in range(len(u_input)):
    time.sleep(30)
    
    user_input=u_input[i]
    print("User:", user_input)
    # Start recorder with the given values
    history.append({"role": "user", "content": user_input})
    bot_output = chatbot(history)
    print("Bot:", bot_output)
    

    history.append({"role": "assistant", "content": bot_output})
    
    
print (history)