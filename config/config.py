import os
from dotenv import load_dotenv
from groq import Groq

# Charger le .env
load_dotenv()

# Initialiser le client Groq
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
# Vous pouvez ajouter d'autres configurations ici si nécessaire