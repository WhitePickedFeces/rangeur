import os
import pathlib
from pathlib import Path   
import shutil
import tkinter as tk
from tkinter import messagebox

# 1. INITIALISATION DE L'INTERFACE GRAPHIQUE
root = tk.Tk()
root.title("Rangement du dossier de téléchargement")

label = tk.Label(root, text="Entrez votre nom d'utilisateur Windows :")
label.pack(padx=10, pady=(10, 5))

entry = tk.Entry(root, width=40)
entry.pack(padx=10, pady=5)


# 2. LA FONCTION PRINCIPALE (Déclenchée par le bouton)
def ranger(event=None):
    name = entry.get().strip()

    # Vérification si le champ est vide
    if not name:
        messagebox.showwarning("Erreur", "Tape ton nom d'utilisateur")
        return

    # Définition des dossiers principaux
    bureau = Path(rf"C:\Users\{name}\OneDrive\Bureau")
    dossier = Path(rf"C:\Users\{name}\Downloads")

    # Vérification si le chemin de l'utilisateur est valide
    if not dossier.exists():
        messagebox.onerror(
            "Erreur", "Le chemin d'accès est introuvable. Vérifiez le nom."
        )
        return

    # CREATION DES DOSSIERS DE DESTINATION (S'ils n'existent pas)
    categories = ["images", "documents", "vidéos", "archives", "audio"]
    for cat in categories:
        chemin_dossier = bureau / cat
        try:
            chemin_dossier.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Impossible de créer le dossier {cat} : {e}")

    # SCANNAGE ET TRI DES FICHIERS
    choise = messagebox.askyesno(
        "Confirmation", "Voulez-vous ranger votre dossier Téléchargements ?")
    if choise:
        print("Début du scan des fichiers de téléchargement...")

        for element in dossier.iterdir():
            if not element.is_file():
                continue

            try:
                # Tri selon les extensions
                if element.suffix.lower() in [".jpg", ".jpeg", ".png",".gif",".webp",]:
                    destination = bureau / "images"
                elif element.suffix.lower() in [".pdf",".docx",".txt",".xlsx",]:
                    destination = bureau / "documents"
                elif element.suffix.lower() in [".mp4", ".mkv", ".avi"]:
                    destination = bureau / "vidéos"
                elif element.suffix.lower() in [".zip", ".rar", ".7z"]:
                    destination = bureau / "archives"
                elif element.suffix.lower() in [".mp3", ".wav"]:
                    destination = bureau / "audio"
                else:
                    continue  # Ignore les fichiers non listés

                # Déplacement effectif du fichier
                shutil.move(str(element), str(destination / element.name))

            except Exception as e:
                print(f"Erreur lors du déplacement du fichier {element.name} : {e}")

        messagebox.showinfo("Succès", "Le rangement est terminé !")


# 3. CREATION DU BOUTON ET LANCEMENT
button = tk.Button(root, text="Ranger", command=ranger)
button.pack(padx=10, pady=10)

root.mainloop()