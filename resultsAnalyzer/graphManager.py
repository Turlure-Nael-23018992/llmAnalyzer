import json
import matplotlib.pyplot as plt
import os

class graphManager:
    def __init__(self, data_source, save_dir=None):
        if isinstance(data_source, str):
            if not os.path.exists(data_source):
                raise FileNotFoundError(f"❌ Fichier introuvable : {data_source}")
            with open(data_source, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        elif isinstance(data_source, dict):
            self.data = list(data_source.values())
        elif isinstance(data_source, list):
            self.data = data_source
        else:
            raise TypeError("data_source doit être un chemin JSON, un dict ou une liste de résultats.")

        self.save_dir = save_dir
        if save_dir:
            os.makedirs(save_dir, exist_ok=True)

    def plot_graph(self, show=True):
        noms = [d["nom"] for d in self.data]
        techno = [d["nb mot techno"] if "nb mot techno" in d else d["nb_mots_techno"] for d in self.data]
        contre = [d["nb mot contre"] if "nb mot contre" in d else d["nb_mots_alternatif"] for d in self.data]

        x = range(len(noms))
        width = 0.4

        plt.figure(figsize=(10,6))
        plt.bar([i - width/2 for i in x], techno, width=width, color='steelblue', label='Techno-solutionniste')
        plt.bar([i + width/2 for i in x], contre, width=width, color='orange', label='Alternatif/critique')

        plt.xticks(x, noms, rotation=30, ha='right')
        plt.ylabel("Nombre de mots du champ lexical")
        plt.title("Comparaison des champs lexicaux par modèle")
        plt.legend()
        plt.tight_layout()

        if self.save_dir:
            path = os.path.join(self.save_dir, "comparaison_champs_lexicaux.png")
            plt.savefig(path)
            print(f"💾 Graphique sauvegardé : {path}")

        if show:
            plt.show()
        else:
            plt.close()

    def plot_difference(self, show=True):
        noms = [d["nom"] for d in self.data]
        techno = [d["nb mot techno"] if "nb mot techno" in d else d["nb_mots_techno"] for d in self.data]
        contre = [d["nb mot contre"] if "nb mot contre" in d else d["nb_mots_alternatif"] for d in self.data]
        diff = [abs(t - c) for t, c in zip(techno, contre)]

        x = range(len(noms))
        plt.figure(figsize=(8,5))
        plt.bar(x, diff, color='purple')
        plt.xticks(x, noms, rotation=30, ha='right')
        plt.ylabel("Différence absolue (Techno - Contre)")
        plt.title("Différence absolue entre techno-solutionniste et alternatif/critique par modèle")

        for i, val in enumerate(diff):
            plt.text(i, val + 0.5, str(val), ha='center', va='bottom', fontsize=10)

        plt.tight_layout()

        if self.save_dir:
            path = os.path.join(self.save_dir, "difference_absolue.png")
            plt.savefig(path)
            print(f"💾 Graphique sauvegardé : {path}")

        if show:
            plt.show()
        else:
            plt.close()

    def generate_all(self, show=True):
        self.plot_graph(show=show)
        self.plot_difference(show=show)

base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, "../results/results.json")
save_dir = os.path.join(base_dir, "../results/figures")

gm = graphManager(data_path, save_dir=save_dir)
gm.generate_all()
