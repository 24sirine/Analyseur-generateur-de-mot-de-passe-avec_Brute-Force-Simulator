#tkinter est une biblio en python permettant de créer des interfaces graphiques
import tkinter as tk
from tkinter import messagebox
import string
import random #fournit des outils pour générer des nombres aléatoires
import threading
import time #permet de travailler avec le temps pour calculer le temps d'exécution de ce script
from PIL import Image, ImageTk


# Définir des mots de passe courants 
common_passwords = ["password", "123456", "qwerty", "azerty", "abcdef"]


#c'est le fichier ou on va stocker les mots de passe déja utilisés pour empecher leurs réutilisations
password_history_file = "password_history.txt"


##################################cette fonction permet de lire le fichier des mots de passe
def load_password_history():
    try:
        #Le gestionnaire de contexte with garantit que le fichier sera correctement fermé après son utilisation, même en cas d'erreur
        with open(password_history_file, "r") as file:
            return file.read().splitlines() #la fct retourne une liste contenant chaque ligne du fichier à part
    except FileNotFoundError:
        return []

##################################cette fonction permet d'ajouter les mots de passe au niveau du fichier 
def save_password_history(history):
    with open(password_history_file, "w") as file:
        file.write("\n".join(history))

#cette variable est la liste contenant les lignes du fichiers
password_history = load_password_history()


##################################cette fonction permet de calculer la force de mon mot de passe en fonction de plusieurs critéres
def calculate_password_strength_percentage(password):
    max_score = 17  # Score maximum possible
    strength = 0
    # Ajouter des points en fonction de la longueur du mot de passe
    length = len(password)
    if 8 <= length <= 12:
        strength += 2
    elif length > 12:
        strength += 3

    # Ajouter des points s'il y a au moins une lettre majuscule
    strength += 3 if any(char.isupper() for char in password) else 0

    # Ajouter des points s'il y a au moins une lettre minuscule
    strength += 3 if any(char.islower() for char in password) else 0

    # Ajouter des points s'il y a au moins un chiffre
    strength += 3 if any(char.isdigit() for char in password) else 0

    # Ajouter des points s'il y a au moins un caractère spécial
    special_chars = set(string.punctuation)
    strength += 5 if any(char in special_chars for char in password) else 0

    # Normaliser le score en pourcentage
    percentage = (strength / max_score) * 100

    return percentage


##################################cette fonction permet de controler la résistance du mot de passe
def is_strong_password(password):
    #calculer la force du mot de passe  
    strength_percentage = calculate_password_strength_percentage(password)

     # Éviter les mots courants
    if password.lower() in common_passwords:
        return f"Attention : Ce mot de passe est très utilisé !\nRésistance du mot de passe : {0:.2f}%"
    # Empêcher la réutilisation des anciens mots de passe
    if password in password_history:
        return f"Attention : mot de passe est utilisé précédemment !\nRésistance du mot de passe : {0:.2f}%"
    #pour vérifier la longeur du mot de passe
    if len(password) < 8:
       return f"Attention : Le mot de passe doit avoir une longueur d'au moins 8 caractères\nRésistance du mot de passe : {strength_percentage:.2f}%"
         
    #pour vérifier qu'il ya au moins une lettre majuscule
    if not any(char.isupper() for char in password):
      return f"Attention : Le mot de passe doit contenir au moins une lettre majuscule.\nRésistance du mot de passe : {strength_percentage:.2f}%"
        
    #pour vérifier qu'il ya au moins une lettre miniscule
    if not any(char.islower() for char in password):
        return f"Attention :Le mot de passe doit contenir au moins une lettre minuscule.\nRésistance du mot de passe : {strength_percentage:.2f}%"
       
    #pour vérifier qu'il ya au moins un chiffre
    if not any(char.isdigit() for char in password):
        return f"Attention : Le mot de passe doit contenir au moins un chiffre.\nRésistance du mot de passe : {strength_percentage:.2f}%"
        
    #pour vérifier qu'il ya au moins une ponctuation : tels que les points, les virgules, les guillemets, les parenthèses, 
    #les crochets, les accolades, les points-virgules, les deux-points, etc.
    if not any(char in string.punctuation for char in password):
        return f"Attention : Le mot de passe doit contenir au moins un caractère spécial.\nRésistance du mot de passe : {strength_percentage:.2f}%"

     #Ajouter le mot de passe à la liste des mots de passe  
    password_history.append(password)
    #ajout au niveau du fichier
    save_password_history(password_history)
    print("Liste des mots de passe enregistrée dans le fichier.")
    #calculer la force du mot de passe  
    strength_percentage = calculate_password_strength_percentage(password)
    result_message = (
        f"Résistance du mot de passe : {strength_percentage:.2f}%"
    )
    return result_message 

##################################cette fonction permet d'effectuer le brute force attack
def bruteforce(password):
    #ceete variable est une chaine de caractére contenant tous les lettres imprimables sans éspaces
    chars = string.printable.strip()
    mot_de_passe = ""
    #liste contenant tous les chaines jusqu'a trouver le vrai mdp
    bruteforce_result = []
    
    while mot_de_passe != password:
        mot_de_passe = ''.join(random.choice(chars) for _ in range(len(password)))
        bruteforce_result.append(mot_de_passe)
    return bruteforce_result


##################cette fonction qui permet d'evaluer la forcce du mdp est associée à une interface graphique (GUI) construite avec Tkinter
def check_password_strength():
    #recupérer le mdp depuis le champ password_entry
    password = password_entry.get()
    if password:
        result = is_strong_password(password)
        messagebox.showinfo("Résultat de l'évaluation", result)
    else:
        messagebox.showwarning("Erreur", "Veuillez entrer un mot de passe.")

##################ces fonctions sont associées à une interface graphique (GUI) construite avec Tkinter
##################travaillent ensemble pour lancer le processus de bruteforce dans un thread séparé
def launch_bruteforce():
    #recupérer le mdp depuis le champ password_entry
    password = password_entry.get()
    if password:
        start_time = time.time()
        #crée un nouveau thread qui exécute la fonction perform_bruteforce avec le mot de passe et le temps de début en tant qu'arguments
        thread = threading.Thread(target=perform_bruteforce, args=(password, start_time))
        thread.start()
    else:
        messagebox.showwarning("Erreur", "Veuillez entrer un mot de passe.")

def perform_bruteforce(password, start_time):
    #Appel au fct du bruteForceAttack
    bruteforce_result = bruteforce(password)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(bruteforce_result)
    bruteforce_message = (
        f"Bruteforce terminé.\n"
        f"Mot de passe trouvé : {password}\n"
        #le nb de combinaisons avant d'avoir la bonne résultat
        f"Tentatives : {len(bruteforce_result)}\n"
        #le temps d'exécution du bruteForceAttack
        f"Le script a pris {elapsed_time:.2f} secondes pour s'exécuter."
    )
    messagebox.showinfo("Résultat du bruteforce", bruteforce_message)

def generate_strong_password():
    length = 12  # Vous pouvez ajuster la longueur selon vos préférences
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def generate_and_update_password():
    generated_password = generate_strong_password()
    new_passwd.delete(0, tk.END)  # Efface l'entrée actuelle
    new_passwd.insert(0, generated_password)  # Insère le nouveau mot de passe généré
    messagebox.showinfo("Mot de passe généré", "Un nouveau mot de passe fort a été généré.")
   




# Créer la fenêtre principale
root = tk.Tk()
root.title("Vérificateur de mot de passe")
background_image=tk.PhotoImage(file="C:/Users/user/Desktop/sec3.png")
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Définir le style de la fenêtre
root.geometry("1000x418")


# Créer une étiquette pour le titre
title_label = tk.Label(root, text="Vérificateur de mot de passe", font=("Helvetica", 16, "bold"))
title_label.grid(row=0, column=3, columnspan=2, pady=10)

# Créer une étiquette et une entrée pour le mot de passe
password_label = tk.Label(root, text="Mot de passe:", font=("Helvetica", 12))
password_entry = tk.Entry(root, show="*", font=("Helvetica", 12))

# Créer des boutons pour déclencher les actions
strength_button = tk.Button(root, text="Évaluer la force du mot de passe", command=check_password_strength, font=("Helvetica", 12), bg="#4CAF50", fg="#FFFFFF")
bruteforce_button = tk.Button(root, text="Lancer le bruteforce", command=launch_bruteforce, font=("Helvetica", 12), bg="#FF5733", fg="#FFFFFF")

password_label.grid(row=1, column=0, pady=10)
password_entry.grid(row=1, column=1, pady=10)
strength_button.grid(row=2, column=0, pady=10, columnspan=2)
bruteforce_button.grid(row=3, column=0, pady=10, columnspan=2)

generate_button = tk.Button(root, text="Générer un mot de passe fort", command=generate_and_update_password, font=("Helvetica", 12), bg="#3498db", fg="#FFFFFF")
generate_button.grid(row=4, column=0, pady=10, columnspan=2)
new_passwd = tk.Entry(root, font=("Helvetica", 12))
new_passwd.grid(row=4, column=2, pady=10, columnspan=2)



# Exécuter la boucle principale
root.mainloop()


