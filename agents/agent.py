from config.config import client

class Agent:
    #Initialisation de l'agent avec un prompt système optionnel
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})
# Appel de l'agent avec un message utilisateur
    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result
# Exécution de la requête auprès du client Groq
    def execute(self):
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            temperature=0,
            messages=self.messages
        )
        return completion.choices[0].message.content
