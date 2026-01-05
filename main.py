import openai
import re
import httpx
import os
from dotenv import load_dotenv
# Load environment variables from a .env file
_ = load_dotenv()
from openai import OpenAI
# Initialize the OpenAI client with the API key from environment variables
client = OpenAI()
# Create a chat completion using the GPT-3.5-turbo model
chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello world"}]
)
# Print the content of the first choice from the chat completion response
chat_completion.choices[0].message.content
# Define an Agent class to interact with the OpenAI API
class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            #Appelle l’API OpenAI avec tout l’historique
            self.messages.append({"role": "system", "content": system})
#rendre l’agent appelable comme une fonction
    def __call__(self, message):
        # Ajouter le message de l'utilisateur aux messages
        self.messages.append({"role": "user", "content": message})
        # Exécuter l'appel à l'API OpenAI
        result = self.execute()
        # Ajouter la réponse de l'assistant aux messages
        self.messages.append({"role": "assistant", "content": result})
        return result
# Méthode pour exécuter l'appel à l'API OpenAI
    def execute(self):
        completion = client.chat.completions.create(
                        model="gpt-4o", 
                        temperature=0,
                        messages=self.messages)
        # Return the content of the first choice from the completion response
        return completion.choices[0].message.content