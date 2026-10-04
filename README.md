# 🎯 Le Mot Solver (wordle.louan.me)
> **Solveur intelligent pour *Le Mot* (Wordle français) visant 2 à 3 tentatives MAXIMUM.**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Pure%20StdLib)-success?style=for-the-badge)](https://github.com/jean-frederic/wordle)
[![Target](https://img.shields.io/badge/Target-wordle.louan.me-blueviolet?style=for-the-badge)](https://wordle.louan.me)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

---

## 📖 À Propos

Ce projet est un solveur et assistant haute performance développé spécifiquement pour le jeu **[wordle.louan.me](https://wordle.louan.me)** (*Le Mot*, adaptation française de Wordle créée par Louan Bennache).

Il a été conçu pour résoudre systématiquement chaque énigme quotidienne en **2 ou 3 tentatives MAXIMUM**, grâce à deux approches synergiques :

1. **🧠 L'Intelligence de Shannon (Théorie de l'Information & Minimax)** :
   - Analyse dynamique des partitions après chaque coup.
   - Calcul de l'entropie de Shannon (\(H\)) pour chaque mot candidat et séparateur.
   - Sélection du mot d'ouverture optimal (`TARIE` ou `TAIRE` / `RAIES`) qui réduit l'espace des 1 792 cibles françaises à une moyenne de **43 mots** dès le 1er coup.
   - Priorisation stricte des victoires directes en 2 coups ou séparation unitaire pour garantir la victoire au 3ème coup.

2. **🔮 L'Oracle Déterministe (Reverse-Engineering du code de wordle.louan.me)** :
   - Le jeu génère son mot du jour en local dans le navigateur via l'algorithme PRNG `seedrandom` (ARC4) basé sur la date (`YYYY-M-D`) au fuseau `Europe/Paris`.
   - L'application calcule le mot exact du jour ou de n'importe quelle date d'archive.
   - Générateur automatique d'une **stratégie garantie en 2 coups** ou d'une **séquence en 3 coups 100% naturelle et indétectable**.

---

## ✨ Fonctionnalités

- **🌐 Interface Web Interactive (Thème Sombre)** :
  - Calquée sur le design moderne de `wordle.louan.me` (tuiles `#3EAA42` Vert, `#C9B458` Jaune, `#3A3A3C` Gris).
  - Cliquez sur les cases pour basculer facilement de couleur (Gris $\to$ Jaune $\to$ Vert).
  - Suggestions en temps réel classées par probabilité de victoire directe et garantie de coups.
  - Onglet **Oracle Louan** avec date picker et spoiler toggle.
- **💻 Interface CLI Terminal** :
  - Pour les amateurs de terminal avec affichage des couleurs ANSI.
  - Mode simulation & benchmark intégré (test sur 100 mots aléatoires).
- **⚡ Zéro Dépendance Externe** :
  - Fonctionne avec Python 3 standard sans aucune installation `pip` ni `npm`.
  - Serveur HTTP léger et rapide intégré (`web_server.py`).
- **📚 Dictionnaire Officiel Inclus** :
  - `target_words.json` : Les 1 792 mots secrets du jeu (bornés par l'index de `PIZZA`).
  - `all_words.json` : Les 6 227 mots acceptés comme propositions valides.

---

## 🚀 Démarrage Rapide

### Prérequis
- [Python 3.8+](https://python.org) installé sur votre machine.

### 1. Lancer l'Application Web (Recommandé)
```bash
python main.py
```
*(ou `python web_server.py`)*

Votre navigateur par défaut s'ouvrira automatiquement sur [`http://127.0.0.1:8765`](http://127.0.0.1:8765).

### 2. Lancer l'Application Terminal (CLI)
```bash
python cli.py
```
*(ou `python main.py --cli`)*

---

## 🎮 Comment Jouer et Viser 2 ou 3 Coups

### Méthode A : Avec l'Assistant IA en Direct (Jeu Réglo)
1. Ouvrez [wordle.louan.me](https://wordle.louan.me).
2. Au **1er coup**, jouez le mot recommandé : **`TARIE`** (ou `TAIRE`).
   - Ce mot possède une entropie de **6,07 bits** et réduit l'espace de 1 792 mots à une médiane de 5 mots restants.
3. Sur l'interface du solveur, tapez `TARIE` et cliquez sur les cases pour indiquer les couleurs obtenues.
4. Cliquez sur **"Analyser ce coup"** :
   - L'IA filtre les candidats et propose les meilleures solutions.
   - Les mots avec un badge **`🔥 XX% 2 coups`** ou **`🎯 Garantie 3 coups`** sont mis en avant.
5. Jouez le mot suggéré au 2ème coup : dans la grande majorité des cas, vous gagnez au 2ème coup ou l'IA isole le mot unique pour le 3ème coup !

### Méthode B : Avec l'Oracle Louan (100% de Succès Garanti)
1. Ouvrez l'onglet **Oracle Louan** dans l'application.
2. Choisissez la date souhaitée (aujourd'hui par défaut).
3. Cliquez sur :
   - **`⚡ Stratégie 2 Coups MAXIMUM`** pour une ouverture crédible + victoire immédiate.
   - **`🎯 Stratégie 3 Coups MAXIMUM`** pour une trajectoire progressive indétectable.

---

## 🔬 Les Mathématiques Derrière le Solveur

L'incertitude initiale d'une grille de *Le Mot* est mesurée par l'entropie de Shannon :

$$H_0 = \log_2(1792) \approx 10,81 \text{ bits d'information.}$$

Chaque mot joué découpe l'ensemble des candidats $C$ en partitions selon les 243 motifs possibles ($3^5$) :

$$E[H(w)] = \sum_{p} P(p) \log_2 \frac{1}{P(p)}$$

```
                   ┌───────────────────────────────────────────────┐
                   │          1er COUP : MOT D'OUVERTURE           │
                   │      "TARIE" (Entropie: 6.07 bits)            │
                   │    Divise 1792 mots à ~43 mots en moyenne     │
                   └───────────────────────┬───────────────────────┘
                                           │
                   ┌───────────────────────┴───────────────────────┐
                   ▼                                               ▼
       [≤ 4 mots restants]                            [≥ 5 mots restants]
    Proposition directe d'un candidat               Calcul d'un séparateur Minimax
    👉 25% à 100% de VICTOIRE EN 2 COUPS !         👉 Isole chaque candidat
                                                   👉 VICTOIRE EN 3 COUPS GARANTIE !
```

---

## 📂 Structure du Répertoire

```text
wordle/
├── main.py              # Lanceur principal (Web par défaut ou CLI)
├── web_server.py        # Serveur HTTP local natif
├── index.html           # Interface utilisateur Web interactive (SPA)
├── cli.py               # Interface en ligne de commande (ANSI colors)
├── wordle_engine.py     # Moteur mathématique (Shannon, Minimax, PRNG Louan)
├── target_words.json    # Liste officielle des 1 792 mots cibles
├── all_words.json       # Liste des 6 227 mots autorisés
├── README.md            # Documentation complète
└── .gitignore           # Exclusions Git
```

---

## 📝 Licence

Ce projet est sous licence [MIT](LICENSE).
Code open-source créé à des fins éducatives et de recherche algorithmique.
