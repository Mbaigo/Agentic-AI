# Fonctions que l’agent peut exécuter
def calculate(expr):
    return eval(expr)
# Fonction pour obtenir le poids moyen
def average_dog_weight(name):
    if name == "Scottish Terrier":
        return "Scottish Terriers average 20 lbs"
    elif name == "Border Collie":
        return "A Border Collie averages 37 lbs"
    elif name == "Toy Poodle":
        return "A Toy Poodle averages 7 lbs"
    else:
        return "An average dog weighs 50 lbs"

# Dictionnaire des actions connues
known_actions = {
    "calculate": calculate,
    "average_dog_weight": average_dog_weight
}
