import json
import os
import re

from lexicalFields import techno_solutionniste, alternatif_critique


class llmTextAnalyzer:
    def __init__(self, index_path, results_path="results/results.json"):
        self.index_path = index_path
        self.results_path = results_path
        self.texts = self._load_index()

    def _load_index(self):
        if not os.path.exists(self.index_path):
            raise FileNotFoundError(f"❌ Fichier {self.index_path} introuvable.")
        with open(self.index_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_text(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def _nombreMots(self, texte, champ):
        texte = texte.lower()
        nb = 0
        for mot in champ:
            mot_escaped = re.escape(mot.lower())
            occurrences = len(re.findall(r"\b" + mot_escaped + r"\b", texte))
            nb += occurrences
        return nb

    def _analyze_text(self, nom, texte):
        nb_total = len(texte.split())
        n1 = self._nombreMots(texte, techno_solutionniste)
        n2 = self._nombreMots(texte, alternatif_critique)
        return {
            "nom": nom,
            "nb_mots_total": nb_total,
            "nb_mots_techno": n1,
            "pourcentage_techno": round((n1 / nb_total) * 100, 2) if nb_total > 0 else 0,
            "nb_mots_alternatif": n2,
            "pourcentage_alternatif": round((n2 / nb_total) * 100, 2) if nb_total > 0 else 0,
        }

    def analyze_all(self):
        results = []
        for entry in self.texts:
            nom = entry["name"]
            path = entry["path"]
            if not os.path.exists(path):
                print(f"⚠️ Fichier manquant : {path}")
                continue
            texte = self._load_text(path)
            stats = self._analyze_text(nom, texte)
            results.append(stats)
            print(f"✅ Analyse terminée pour {nom}")
        self._save_results(results)
        return results

    def _save_results(self, results):
        with open(self.results_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        print(f"💾 Résultats enregistrés dans {self.results_path}")
        
        
analyzer = llmTextAnalyzer("texts/index.json")
results = analyzer.analyze_all()

for r in results:
    print(f"{r['nom']} : {r['pourcentage_techno']}% techno / {r['pourcentage_alternatif']}% alternatif")
