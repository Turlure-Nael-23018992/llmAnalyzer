import os
import json

class textManager:
    
    def __init__(self, file):
        self.file = file
        if os.path.exists(self.file):
            with open(self.file, "r", encoding="utf-8") as f:
                try:
                    self.textList = json.load(f)
                except json.JSONDecodeError:
                    self.textList = []
        else:
            self.textList = []
            self._save()

    def _save(self):
        """Sauvegarde la liste actuelle dans le fichier JSON"""
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.textList, f, indent=4, ensure_ascii=False)

    def addToJson(self, name, path):
        """
        Ajoute un nouveau texte à l’index s’il n’existe pas déjà.
        name : nom du texte (ex : 'gpt')
        path : chemin du fichier texte (ex : 'texts/gpt.txt')
        """
        if any(entry["name"] == name for entry in self.textList):
            print(f"⚠️ Le texte '{name}' est déjà présent dans {self.file}.")
            return
        
        entry = {
            "name": name,
            "filename": os.path.basename(path),
            "path": path
        }
        self.textList.append(entry)
        self._save()
        print(f"✅ '{name}' ajouté à {self.file}.")

    def listTexts(self):
        """Affiche la liste des textes enregistrés"""
        if not self.textList:
            print("Aucun texte enregistré.")
        else:
            print("Textes enregistrés :")
            for entry in self.textList:
                print(f"- {entry['name']} → {entry['path']}")

    def getTexts(self):
        """Retourne la liste complète (utile pour des analyses automatisées)"""
        return self.textList

tm = textManager("texts/index.json")

# Boucler sur tous les fichiers .txt du dossier
for filename in os.listdir("texts"):
    if filename.endswith(".txt"):
        path = os.path.join("texts", filename)
        name = os.path.splitext(filename)[0]  # nom sans extension, ex: "gpt"
        tm.addToJson(name, path)

# Afficher le contenu final de l’index
tm.listTexts()

# Affichage simple des chemins
for entry in tm.getTexts():
    print(entry["name"], "→", entry["path"])


