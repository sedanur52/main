import tkinter as tk
from tkinter import messagebox
import psycopg2
import speech_recognition as sr
import tkinter as tk
import re
from tkinter import *

root = tk.Tk()
root.title("Interface de connexion :")
root.configure(background="#f7f7f7")

conn = psycopg2.connect(
          user = "postgres",
          password = "system",
          host = "localhost",
          port = "5432",
          database = "CDP"
)
cur = conn.cursor()

def register():
    username = username_entry.get()
    password = password_entry.get()
    cur = conn.cursor()
    cur.execute("SELECT name FROM users WHERE name=%s", (username,))
    existing_user = cur.fetchone()
    if existing_user:
         error_label.config(text="Erreur : Nom d'utilisateur déjà existant.", fg="red")
         return

    cur.execute("INSERT INTO users (name, password, role) VALUES (%s, %s, %s)", (username, password, "client"))
    conn.commit()
    error_label.config(text="Succès : Utilisateur enregistré avec succès.", fg="green")

def enregistrer_informations(nom, prenom, email, contact, consentement, age, num_secu):
    cur.execute("INSERT INTO informations (ID, Nom, Prenom, Email, Contact, Consentement,Age, Num_secu )  VALUES (nextval('Id_sequence'), %s, %s, %s, %s, %s, %s, %s)",
                (nom, prenom, email, contact, consentement, age, num_secu))
    conn.commit()
    
def saisie_vocale():
    nom = None
    prenom = None
    email = None
    age = None
    contact = None
    consentement = None
    num_secu = None
    r = sr.Recognizer()
    with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5) # Elimination du bruit ambiant
                try:
                    print(" Dites votre nom : ")
                    nom = r.recognize_google(r.listen(source), language='fr-FR')
                    while(any(char.isdigit() for char in nom)):
                        print("Vous devez saisir un nom sous forme d'une chaîne de caractères")
                        print(" Dites votre nom : ")
                        nom = r.recognize_google(r.listen(source), language='fr-FR')
                    
                    print(" Dites votre prénom : ")
                    prenom = r.recognize_google(r.listen(source), language='fr-FR')
                    while(any(char.isdigit() for char in prenom)):
                        print(" Vous devez saisir un prénom sous forme d'une chaîne de caractères")
                        print(" Dites votre prénom : ")
                        prenom = r.recognize_google(r.listen(source), language='fr-FR')
                           
                    print(" Dites votre email : ")
                    email = r.recognize_google(r.listen(source), language='fr-FR')
                    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
                    while True:
                        if( not re.match(pattern, email)):
                            print("L'adresse email saisie n'est pas valide.")
                            print(" Dites votre email : ")
                            email = r.recognize_google(r.listen(source), language='fr-FR')
                        else:
                            break
                        
                    print(" Dites votre âge : ")
                    age = r.recognize_google(r.listen(source), language='fr-FR')  
                    while True:
                        if(re.match(r'^\d+$',age)):
                                # age = int(age)
                                break
                        else:
                            print("Vous devez saisir un nombre entier.")
                            print(" Dites votre âge : ")
                            age = r.recognize_google(r.listen(source), language='fr-FR')  
                        
                    print(" Dites votre numéro de téléphone : ")
                    contact = r.recognize_google(r.listen(source), language='fr-FR')  
                    
                    contact  = contact .replace(' ', '') # remove all spaces from the input string
                    while(True):
                        if(re.match(r'^\d{10}$', contact)):
                          #  contact  = int(contact )
                            break
                        else:
                            print(" Vous devez saisir un numéro de téléphone valide, composé de 10 chiffres. ")
                            print(" Dites votre numéro de téléphone : ")
                            contact = r.recognize_google(r.listen(source), language='fr-FR') 
                            contact  = contact .replace(' ', '') # remove all spaces from the input string 
                            
                     
                    print(" Dites oui ou non pour le consentement : ")
                    consentement = r.recognize_google(r.listen(source), language='fr-FR') 
                    while(any(char.isdigit() for char in consentement)):  
                         print(" Dites juste Oui ou Non ")
                         print("Dites oui ou non pour le consentement : ")
                         consentement = r.recognize_google(r.listen(source), language='fr-FR') 
                       
                    print(" Dites votre numéro de sécurité sociale : ")
                    num_secu = r.recognize_google(r.listen(source), language='fr-FR')
                    num_secu = num_secu.replace(" ", "") # Remove any spaces
                    while True:
                        if(not num_secu.isnumeric() or len(num_secu) != 13):
                            print(" Veuillez saisir une valeurs numérique de 13 chiffre  ")
                            print(" Dites votre numéro de sécurité sociale : ")
                            num_secu = r.recognize_google(r.listen(source), language='fr-FR')
                            num_secu = num_secu.replace(" ", "") # Remove any spaces
                        else:
                            break
                except sr.UnknownValueError:
                     print("Je n'ai pas compris ce que vous avez dit. Veuillez répéter.")
                except sr.RequestError as e:
                    print("Impossible de se connecter au service de reconnaissance vocale. Veuillez vérifier votre connexion internet.")
                except KeyboardInterrupt:
                    print("Interruption de l'utilisateur.")
                    return None
    return nom, prenom, email, age, contact, consentement, num_secu
   

def afficher_informations(nom, prenom, email, contact, consentement , age, num_secu):
    nom_label.config(text=" Nom: " + nom)
    prenom_label.config(text=" Prénom: " + prenom)
    email_label.config(text=" Email: " + email)
    age_label.config(text=" Âge: " + age)
    contact_label.config(text=" Personne à contacter: " + contact)
    consentement_label.config(text=" Consentement: " + consentement)
    num_secu_label.config(text=" Numéro de sécurité sociale: " + str(num_secu))
    
    
def saisie_et_affichage():
    nom, prenom, email,age,contact,consentement,num_secu = saisie_vocale()
    email = email.replace(" ", "")
    num_secu = num_secu.replace(" ", "")
    num_secu = int(num_secu)
    enregistrer_informations(nom, prenom, email, contact, consentement, age, num_secu)
    afficher_informations(nom, prenom, email, contact, consentement , age, num_secu)
   
    
def login():
    username = username_entry.get()
    password = password_entry.get()
    # Vérifie les informations d'identification entrées contre les informations d'identification stockées dans la base de données
    cur = conn.cursor()
    cur.execute(" SELECT role FROM users WHERE Name = %s AND Password = %s ", (username, password))
    result = cur.fetchone()
    if result is None:
        welcome_label.config(text="Bienvenue, " + username + "!", fg="black")
        logged_in_user.config(text="Connecté en tant que: " + username, fg="#00a1ff")
        error_label.config(text="Nom d'utilisateur ou mot de passe incorrect .\n si vous avez pas de compte cliquer sur s'enregistrer", fg="red")
    elif result[0] == "client":
        root = tk.Tk()
        root.geometry("600x500")
         # Labels for each field
        global nom_label
        nom_label = tk.Label(root, text=" Dicter votre Nom : ", font=("Arial", 12))
        nom_label.grid(row=0, column=0, padx=10, pady=10)
        global prenom_label
        prenom_label = tk.Label(root, text="Dicter votre Prénom: ", font=("Arial", 12))
        prenom_label.grid(row=1, column=0, padx=10, pady=10)
        global email_label
        email_label = tk.Label(root, text="Dicter votre Email: ", font=("Arial", 12))
        email_label.grid(row=2, column=0, padx=10, pady=10)
        global age_label
        age_label = tk.Label(root, text="Dicter votre  Âge: ", font=("Arial", 12))
        age_label.grid(row=3, column=0, padx=10, pady=10)
       
        global contact_label
        contact_label  = tk.Label(root, text=" Dicter votre Numéro d'une personne à contacter : ", font=("Arial", 12))
        contact_label.grid(row=4, column=0, padx=10, pady=10)
        global consentement_label
        consentement_label  = tk.Label(root, text=" Le consentement:(Oui ou Non) ", font=("Arial", 12))
        consentement_label.grid(row=5, column=0, padx=10, pady=10)
        
        global num_secu_label
        num_secu_label = tk.Label(root, text="Dicter votre Numéro de sécurité sociale: ", font=("Arial", 12))
        num_secu_label.grid(row=6, column=0, padx=10, pady=10)
       # Button for submitting the form
        submit_button = tk.Button(root, text=" Saisie Vocale ", font=("Arial", 12), bg="purple", fg="white", command=saisie_et_affichage)
        submit_button.grid(row=7, column=1, pady=20)
        
    elif result[0] == "admin":
        cur.execute("SELECT * FROM informations")
        all_info = cur.fetchall()
        if all_info:
            
            info_window = tk.Tk()
            info_window.title("Informations des utilisateurs")
            info_window.geometry("900x500")
            info_window.configure(background="#f7f7f7")
            info_table = tk.Frame(info_window)
            info_table.pack()
            info_table_headers = ["ID", "Nom", "Prénom", "Email", " Téléphone", " Consentement ","Age", " Numéro de sécurité Sociale "]
            for header_index, header_text in enumerate(info_table_headers):
                header_label = tk.Label(info_table, text=header_text, font=("Arial", 14, "bold"), padx=10, pady=5, relief=tk.RIDGE, bg="#eaeaea")
                header_label.grid(row=0, column=header_index, sticky="nsew")
            for row_index, row_data in enumerate(all_info):
                for column_index, cell_data in enumerate(row_data):
                    cell_label = tk.Label(info_table, text=str(cell_data), font=("Arial", 12), padx=10, pady=5, relief=tk.RIDGE)
                    cell_label.grid(row=row_index+1, column=column_index, sticky="nsew")
    else:
        # Rediriger vers une autre page si le rôle n'est pas "client"
        error_label.config(text=" Nom d'utilisateur ou mot de passe incorrect si vous avez pas de compte cliquer sur enregistrer ", fg="red")
        messagebox.showerror("Erreur", "Rôle utilisateur inconnu. Veuillez contacter l'administrateur.")
        pass

title_label = tk.Label(root, text="Remplir vos formulaires avec votre voix \n", font=("Arial", 16), fg="purple")
title_label.pack(pady=20)

# Crée un widget Frame pour le formulaire de connexion
login_frame = tk.Frame(root)
login_frame.pack()

# Crée un widget Label et Entry pour le nom d'utilisateur
username_label = tk.Label(login_frame, text="Nom d'utilisateur:")
username_label.pack(side=tk.LEFT, padx=10)
username_entry = tk.Entry(login_frame)
username_entry.pack(side=tk.LEFT)

# Crée un widget Label et Entry pour le mot de passe
password_label = tk.Label(login_frame, text="Mot de passe:")
password_label.pack(side=tk.LEFT, padx=10)
password_entry = tk.Entry(login_frame, show="*")
password_entry.pack(side=tk.LEFT)

# Crée un widget Button pour se connecter
login_button = tk.Button(root, text="Se connecter", command=login)
login_button.pack(pady=10)

register_button = tk.Button(root, text="S'enregistrer ", command=register)
register_button.pack(pady=10)
# Crée un widget Label pour afficher les erreurs
error_label = tk.Label(root, fg="red")
error_label.pack()

# Crée un widget Label pour afficher un message de bienvenue
welcome_label = tk.Label(root, font=("Arial", 14))
welcome_label.pack(pady=20)

# Crée un widget Label pour afficher les informations de l'utilisateur connecté
logged_in_user = tk.Label(root)
logged_in_user.pack()

# Lance la boucle principale de l'interface utilisateur
root.mainloop()
