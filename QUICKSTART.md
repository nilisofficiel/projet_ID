# Guide de Démarrage Rapide

Ce guide vous aidera à démarrer rapidement avec le système de création de télé-réalité animée.

## ⚡ Installation Rapide (5 minutes)

### 1. Installer les Prérequis

```bash
# Installer Python 3.8+ (si non installé)
# Sur Ubuntu/Debian:
sudo apt update
sudo apt install python3 python3-pip

# Installer FFmpeg
sudo apt install ffmpeg
```

### 2. Cloner et Installer

```bash
# Cloner le repository
git clone https://github.com/nilisofficiel/projet_ID.git
cd projet_ID

# Installer les dépendances Python
pip install -r requirements.txt
```

### 3. Configurer les Clés API

```bash
# Copier le template d'environnement
cp .env.template .env

# Éditer .env avec vos clés API
nano .env  # ou utilisez votre éditeur préféré
```

Remplir au minimum:
- `HUGGINGFACE_API_KEY` - Obtenir sur [huggingface.co](https://huggingface.co/settings/tokens)
- `DID_API_KEY` - Obtenir sur [d-id.com](https://studio.d-id.com/account-settings)

## 🚀 Créer Votre Premier Épisode (2 minutes)

### Option 1: Ligne de Commande (Le Plus Simple)

```bash
cd Scripts
python reality_show_workflow.py photo1.jpg photo2.jpg photo3.jpg
```

L'épisode sera créé automatiquement dans `output/episodes/`

### Option 2: Script Python Personnalisé

Créer un fichier `mon_episode.py`:

```python
from Scripts.reality_show_workflow import RealityShowProducer

# Initialiser
producer = RealityShowProducer()

# Créer l'épisode
episode = producer.quick_episode_from_images(
    image_paths=['photo1.jpg', 'photo2.jpg'],
    episode_name='mon_premier_episode',
    platform='tiktok'
)

print(f"Épisode créé: {episode}")
```

Puis exécuter:
```bash
python mon_episode.py
```

## 📸 Où Trouver des Images?

Pour tester le système, vous pouvez:

1. **Utiliser vos propres photos** (format JPG ou PNG)
2. **Télécharger des images libres de droits** depuis:
   - [Unsplash](https://unsplash.com/)
   - [Pexels](https://www.pexels.com/)
   - [Pixabay](https://pixabay.com/)

**Important**: Assurez-vous d'avoir les droits nécessaires pour utiliser les images.

## 🎬 Structure d'un Épisode

### Scénario Simple (3 scènes)

```python
scenes = [
    # Scène 1: Introduction
    {
        'influencer_images': ['influencer1.jpg'],
        'expressions': ['happy'],
        'duration': 10
    },

    # Scène 2: Rencontre
    {
        'influencer_images': ['influencer1.jpg', 'influencer2.jpg'],
        'expressions': ['surprised', 'happy'],
        'duration': 15
    },

    # Scène 3: Conclusion
    {
        'influencer_images': ['influencer1.jpg', 'influencer2.jpg'],
        'expressions': ['happy', 'happy'],
        'duration': 10
    }
]

producer.create_episode(
    episode_name='episode_01',
    scenes=scenes,
    platform='tiktok'
)
```

## 🎵 Ajouter de la Musique

```python
episode = producer.create_episode(
    episode_name='episode_avec_musique',
    scenes=scenes,
    background_music='chemin/vers/musique.mp3',  # Ajoutez votre musique
    platform='tiktok'
)
```

## 📱 Plateformes Supportées

Le système optimise automatiquement pour:
- `tiktok` - 1080x1920 (vertical)
- `instagram` - 1080x1920 (vertical)
- `youtube` - 1920x1080 (horizontal)

## 🔍 Vérifier Votre Installation

Tester que tout fonctionne:

```bash
# Vérifier Python
python3 --version  # Doit être >= 3.8

# Vérifier FFmpeg
ffmpeg -version

# Vérifier les dépendances Python
pip list | grep -E "requests|Pillow|opencv"
```

## 📂 Où Trouver les Fichiers Générés?

Après création, vos fichiers seront dans:
```
output/
├── avatars/          # Avatars cartoonisés
├── animations/       # Animations individuelles
└── episodes/         # Épisodes finaux prêts à publier
```

## ❗ Problèmes Courants

### "FFmpeg not found"
```bash
# Installer FFmpeg
sudo apt install ffmpeg  # Ubuntu/Debian
brew install ffmpeg      # macOS
```

### "API key is required"
Vérifier que le fichier `.env` contient vos clés API:
```bash
cat .env  # Afficher le contenu
```

### "Module not found"
```bash
# Réinstaller les dépendances
pip install -r requirements.txt
```

## 📖 Prochaines Étapes

1. ✅ Créer votre premier épisode de test
2. 📝 Lire la [documentation complète](README.md)
3. 🎨 Explorer les [exemples](Scripts/examples.py)
4. 🚀 Commencer à produire régulièrement!

## 💡 Conseils pour Débuter

1. **Commencez simple**: Un épisode avec 2-3 images seulement
2. **Testez sans musique d'abord**: Ajoutez la musique après
3. **Vérifiez la qualité**: Regardez l'épisode avant de publier
4. **Itérez rapidement**: Créez plusieurs versions courtes

## 🆘 Besoin d'Aide?

- Consultez le [README complet](README.md)
- Vérifiez les [exemples](Scripts/examples.py)
- Ouvrez une issue sur GitHub

---

**Bon démarrage! 🎬✨**
