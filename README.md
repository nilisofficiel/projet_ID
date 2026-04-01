# Projet Télé-Réalité Animée avec Avatars d'Influenceurs

Ce projet permet de créer une **télé-réalité animée** où des avatars dessinés d'influenceurs interagissent dans des histoires scénarisées. Le système transforme automatiquement des photos en avatars stylisés, les anime avec des expressions faciales, et produit des vidéos courtes optimisées pour les réseaux sociaux.

## 🎯 Objectifs du Projet

1. **Transformer** des photos ou vidéos d'influenceurs en avatars dessinés stylisés
2. **Animer** ces avatars avec des expressions faciales et mouvements corporels
3. **Produire** des vidéos courtes (2-3 minutes) optimisées pour TikTok, Instagram Reels, et YouTube Shorts
4. **Publier** des épisodes quotidiens de manière automatisée

## 🚀 Fonctionnalités

### 1. Création d'Avatars (avatar_cartoonizer.py)
- Transformation d'images en style cartoon via **Toonify (Hugging Face)**
- Support pour le traitement par lot de plusieurs images
- Personnalisation des styles d'avatars

### 2. Animation d'Avatars (avatar_animator.py)
- Animation faciale avec **D-ID API**
- Expressions personnalisables (heureux, surpris, neutre, etc.)
- Support pour l'animation de mouvements corporels via **DeepMotion**
- Composition de scènes multi-avatars avec **Runway ML**

### 3. Montage Vidéo (video_editor.py)
- Concaténation de clips vidéo
- Ajout de musique de fond et effets sonores
- Transitions entre scènes
- Optimisation automatique pour différentes plateformes sociales

### 4. Workflow Complet (reality_show_workflow.py)
- Orchestration complète du pipeline de production
- Création d'épisodes à partir de configurations de scènes
- Production par lot de plusieurs épisodes
- Sauvegarde et chargement de projets

## 📋 Prérequis

### Logiciels Requis
- Python 3.8 ou supérieur
- FFmpeg (pour le montage vidéo)

### Clés API Nécessaires
- **Hugging Face API Key** (pour Toonify) - optionnel mais recommandé
- **D-ID API Key** (pour l'animation d'avatars)
- **DeepMotion API Key** (optionnel, pour animations corporelles)

## 🔧 Installation

### 1. Cloner le Repository
```bash
git clone https://github.com/nilisofficiel/projet_ID.git
cd projet_ID
```

### 2. Installer les Dépendances
```bash
pip install -r requirements.txt
```

### 3. Installer FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Télécharger depuis [ffmpeg.org](https://ffmpeg.org/download.html)

### 4. Configurer les Clés API

Créer un fichier `.env` à la racine du projet:
```bash
HUGGINGFACE_API_KEY=votre_cle_huggingface
DID_API_KEY=votre_cle_did
```

Ou créer un fichier `config/reality_show_config.json`:
```json
{
  "huggingface_api_key": "votre_cle_huggingface",
  "did_api_key": "votre_cle_did",
  "default_platform": "tiktok",
  "episode_duration": 180
}
```

## 💡 Utilisation

### Exemple Rapide - Créer un Épisode

```bash
cd Scripts
python reality_show_workflow.py photo1.jpg photo2.jpg photo3.jpg
```

Cela créera automatiquement:
1. Des avatars stylisés à partir des photos
2. Des animations pour chaque avatar
3. Un épisode complet optimisé pour TikTok

### Utilisation Programmée

```python
from Scripts.reality_show_workflow import RealityShowProducer

# Initialiser le producteur
producer = RealityShowProducer()

# Définir les scènes de l'épisode
scenes = [
    {
        'influencer_images': ['influencer1.jpg'],
        'expressions': ['happy'],
        'script': None,  # Pas de dialogue vocal
        'duration': 10
    },
    {
        'influencer_images': ['influencer2.jpg', 'influencer3.jpg'],
        'expressions': ['surprised', 'neutral'],
        'duration': 15
    }
]

# Créer l'épisode
episode = producer.create_episode(
    episode_name='episode_01',
    scenes=scenes,
    background_music='music/background.mp3',
    platform='tiktok'
)

print(f"Épisode créé: {episode}")
```

### Utilisation des Modules Individuels

#### 1. Cartooniser une Image
```python
from Scripts.avatar_cartoonizer import AvatarCartoonizer

cartoonizer = AvatarCartoonizer()
avatar = cartoonizer.cartoonize_with_huggingface(
    'influencer.jpg',
    'mon_avatar'
)
```

#### 2. Animer un Avatar
```python
from Scripts.avatar_animator import AvatarAnimator

animator = AvatarAnimator()
animation = animator.animate_with_did(
    'avatar.png',
    expression='happy',
    output_name='animation_joyeuse'
)
```

#### 3. Monter des Vidéos
```python
from Scripts.video_editor import VideoEditor

editor = VideoEditor()

# Combiner plusieurs clips
episode = editor.concatenate_videos(
    ['clip1.mp4', 'clip2.mp4', 'clip3.mp4'],
    output_name='episode_complet'
)

# Ajouter de la musique
episode_with_music = editor.add_audio(
    episode,
    'background_music.mp3',
    audio_volume=0.3
)

# Optimiser pour TikTok
final = editor.optimize_for_social_media(
    episode_with_music,
    platform='tiktok'
)
```

## 📁 Structure du Projet

```
projet_ID/
├── Scripts/
│   ├── avatar_cartoonizer.py    # Création d'avatars stylisés
│   ├── avatar_animator.py       # Animation des avatars
│   ├── video_editor.py          # Montage vidéo
│   ├── reality_show_workflow.py # Workflow complet
│   ├── csv_to_*.py              # Scripts CSV (legacy)
│   └── workflows/               # Workflows automatisés
├── Data/                        # Données CSV (legacy)
├── output/
│   ├── avatars/                 # Avatars générés
│   ├── animations/              # Animations générées
│   └── episodes/                # Épisodes finaux
├── projects/                    # Configurations de projets sauvegardés
├── config/                      # Fichiers de configuration
├── requirements.txt             # Dépendances Python
└── README.md                    # Cette documentation
```

## 🛠️ Outils et Services Utilisés

### Création d'Avatars
- **[Toonify (Hugging Face)](https://huggingface.co/spaces/akhaliq/Toonify)** - Transformation en style cartoon
- **[Artbreeder](https://www.artbreeder.com/)** - Alternative pour création d'avatars
- **[Fotor Cartoonizer](https://www.fotor.com/features/cartoon.html)** - Filtre cartoon simple

### Animation
- **[D-ID](https://www.d-id.com/)** - Animation faciale et lip sync
- **[DeepMotion Animate 3D](https://www.deepmotion.com/)** - Mouvements corporels
- **[Runway ML](https://runwayml.com/)** - Composition de scènes multiples

### Montage et Publication
- **FFmpeg** - Traitement vidéo professionnel
- **[CapCut](https://www.capcut.com/)** - Alternative pour montage manuel
- **[Epidemic Sound](https://www.epidemicsound.com/)** - Musique libre de droits
- **[Artlist.io](https://artlist.io/)** - Bibliothèque musicale

## ⏱️ Temps de Production Estimé

Pour un épisode de 2-3 minutes:
- **Création des avatars**: 5-10 minutes par avatar
- **Animation et mouvements**: 10-20 minutes par scène
- **Montage et effets finaux**: 30 minutes
- **Total**: ~2 heures pour un épisode complet

## 📱 Plateformes Supportées

Le système optimise automatiquement les vidéos pour:
- **TikTok** (1080x1920, format vertical)
- **Instagram Reels** (1080x1920, format vertical)
- **YouTube Shorts** (1920x1080, format horizontal)

## 🔐 Sécurité et Vie Privée

- Les avatars sont stylisés pour éviter la copie exacte de la morphologie
- Aucune voix originale n'est utilisée
- Les clés API doivent être gardées confidentielles
- Ne jamais committer le fichier `.env` dans Git

## 🤝 Contribution

Les contributions sont les bienvenues! Pour contribuer:

1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commiter vos changements (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrir une Pull Request

## 📝 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support et Questions

Pour toute question ou problème:
- Ouvrir une issue sur GitHub
- Consulter la documentation des APIs utilisées
- Vérifier que toutes les dépendances sont correctement installées

## 🎬 Workflow Complet Pas-à-Pas

### Étape 1: Préparation
1. Collecter les photos des influenceurs
2. Préparer le scénario et les dialogues
3. Choisir la musique de fond

### Étape 2: Production
```bash
# Créer l'épisode
python Scripts/reality_show_workflow.py influencer1.jpg influencer2.jpg
```

### Étape 3: Vérification
1. Visionner l'épisode généré dans `output/episodes/`
2. Vérifier la qualité des animations
3. Ajuster si nécessaire

### Étape 4: Publication
1. Uploader sur la plateforme choisie (TikTok, Instagram, YouTube)
2. Ajouter titre, description et hashtags
3. Programmer la publication

### Étape 5: Itération
1. Analyser les performances
2. Créer le prochain épisode
3. Maintenir un rythme de publication régulier

## 🌟 Exemples de Scénarios

### Scénario 1: Rencontre Surprise
```python
scenes = [
    {
        'influencer_images': ['influencer1.jpg'],
        'expressions': ['happy'],
        'duration': 5
    },
    {
        'influencer_images': ['influencer2.jpg'],
        'expressions': ['surprised'],
        'duration': 5
    },
    {
        'influencer_images': ['influencer1.jpg', 'influencer2.jpg'],
        'expressions': ['happy', 'happy'],
        'duration': 10
    }
]
```

### Scénario 2: Compétition Amicale
```python
scenes = [
    {
        'influencer_images': ['influencer1.jpg'],
        'expressions': ['neutral'],
        'duration': 5
    },
    {
        'influencer_images': ['influencer2.jpg'],
        'expressions': ['neutral'],
        'duration': 5
    },
    {
        'influencer_images': ['influencer1.jpg'],
        'expressions': ['happy'],
        'duration': 5
    }
]
```

---

**Bon courage avec votre télé-réalité animée! 🎬✨**
