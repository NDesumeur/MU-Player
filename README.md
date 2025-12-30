# MU Player 

Un lecteur de musique premium moderne avec interface GUI personnalisable, support YouTube, et contrôle à distance via API web.

---

##  Vue d'ensemble

**MU Player** est une application de lecteur de musique développée en Python avec une interface graphique Tkinter. Elle offre une expérience utilisateur riche avec 25 thèmes personnalisés, gestion de playlists, recommandations musicales, et un serveur web pour contrôler la musique à distance.

---

##  Structure du fichier main.py

### 1. **Importations et Initialisation**

Le fichier commence par importer les bibliothèques essentielles :

- **`tkinter`** : Interface graphique (widgets, dialogs, layout)
- **`pygame`** : Lecture audio et gestion des événements musicaux
- **`pytubefix`** : Téléchargement de vidéos YouTube
- **`mutagen`** : Lecture et manipulation des métadonnées MP3 (ID3 tags)
- **`PIL`** : Traitement et redimensionnement d'images (pochettes)
- **`moviepy`** : Conversion de fichiers audio (WebM → MP3)
- **`flask`** : Serveur web pour l'API de contrôle à distance (optionnel)
- **`plyer`** : Notifications système
- **`youtubesearchpython`** : Recherche de vidéos YouTube
- **`requests`** : Téléchargement de ressources web

```python
import tkinter as tk
from pytubefix import YouTube
import pygame
from mutagen.mp3 import MP3
from PIL import Image, ImageTk
from flask import Flask, request, jsonify  # Optionnel
```

### 2. **Dictionnaire THEMES**

Contient 25 thèmes colorés avec des palettes cohérentes :

```python
THEMES = {
    "Purple Dream": { "main_bg": "#0a0508", "accent": "#a370f7", ... },
    "Deep Blue": { "main_bg": "#0a1628", "accent": "#4da6ff", ... },
    "Dracula": { "main_bg": "#0b0a10", "accent": "#bd93f9", ... },
    # ... 22 autres thèmes
}
```

Chaque thème définit :
- `main_bg` : Couleur de fond principal
- `accent` : Couleur d'accentuation (boutons actifs)
- `text` : Couleur du texte principal
- `progress` : Couleur de la barre de progression
- Et autres variables de style

### 3. **Classes Personnalisées et Widgets**

#### **CustomUrlDialog / CustomDialog / CustomYesNoDialog**
Dialogues modernes pour entrer du texte ou confirmer des actions :
- Entrée d'URLs YouTube
- Confirmation de suppression
- Saisie de noms de playlists

```python
class CustomUrlDialog(tk.Toplevel):
    """Dialogue pour entrer une URL YouTube avec style personnalisé"""
```

#### **ProgressBar**
Barre de progression interactive pour la lecture musicale :
- Cliquable pour chercher (seek) dans la chanson
- Glissable pour contrôle fluide
- Affiche un curseur stylisé

```python
class ProgressBar(tk.Canvas):
    def set_progress(self, value):
        """Met à jour la progression (0.0 à 1.0)"""
    
    def on_click(self, event):
        """Traite les clics pour le seek"""
```

#### **CustomScale**
Curseur personnalisé pour le volume :
- Interface graphique moderne
- Feedback visuel avec couleurs du thème

#### **ModernVolumeSlider**
Curseur spécialisé pour le contrôle du volume :
- Intégré dans la barre de contrôle
- Support du glisser-déplacer

### 4. **Classe Principale : MusicPlayer**

La classe centrale qui gère toute l'application.

#### **Initialisation (`__init__`)**

Le constructeur crée l'interface complète et initialise les composants :

```python
def __init__(self, master):
    self.master = master
    self.master.attributes('-fullscreen', True)
    self.load_settings()
```

**Étapes principales :**
1. Chargement des paramètres (thème, volume, taille polices)
2. Initialisation de pygame pour l'audio
3. Création de la structure d'interface avec Tkinter
4. Configuration des événements clavier (espace, flèches)
5. Démarrage du serveur Flask (si disponible)

**Composants d'interface créés :**

##### **Barre latérale (Sidebar)**
- Logo et titre "MU Player"
- Sélecteur de playlists (OptionMenu)
- Boutons : "Nouvelle playlist", "Paramètres"
- Options de tri (par date, alphabétique, auteur, etc.)

##### **Zone centrale (Center Frame)**
- **Section "Now Playing"** :
  - Pochette de l'album (150×150px)
  - Titre et artiste de la chanson
  - Durée actuelle / totale
  - Barre de progression interactive
  
- **Section "Recommandations"** :
  - Suggestion de chanson suivante basée sur le genre
  - Bouton pour ajouter la recommandation

- **Liste des morceaux** :
  - Affichage numéroté des chansons
  - Durée de chaque chanson
  - Indicateur ❤ pour les favoris

##### **Barre de contrôle (Control Bar)**
- **Boutons de lecture** : 
  - ⏮ Chanson précédente
  - ▶ Lecture
  - ⏸ Pause
  - ▶▶ Reprendre
  - ⏭ Chanson suivante
  
- **Boutons spécialisés** :
  - 🔀 Lecture aléatoire
  - ❤ Toggle favoris
  
- **Boutons d'action** :
  - 📁 Ajouter fichiers
  - 🎬 Ajouter depuis YouTube
  - 🔍 Rechercher
  - 🗑 Supprimer
  
- **Curseur de volume** : Contrôle du volume audio

#### **Gestion des Playlists**

```python
def load_playlist_names(self):
    """Charge la liste des playlists depuis jsons/playlists.json"""

def new_playlist(self):
    """Crée une nouvelle playlist"""

def load_new_playlist(self, *args):
    """Change la playlist active et récharge la liste"""

def load_metadata(self):
    """Charge les métadonnées (titre, artiste, durée) pour chaque chanson"""
```

Chaque playlist a :
- Un fichier JSON dédié : `jsons/metadata_[NOM].json`
- Une playlist "Favoris" par défaut (non supprimable)
- Métadonnées : titre, artiste, URL, date ajout, nombre d'écoutes, etc.

#### **Lecture Audio**

```python
def play_song(self):
    """Lance la lecture de la chanson sélectionnée"""

def pause_song(self):
    """Met en pause la lecture"""

def unpause_song(self):
    """Reprend la lecture après une pause"""

def play_next_song(self):
    """Passe à la chanson suivante (boucle)"""

def play_previous_song(self):
    """Revient à la chanson précédente"""

def shuffle_play(self):
    """Lance la lecture en mode aléatoire"""

def on_progress_click(self, progress):
    """Cherche à une position dans la chanson (seek)"""

def update_song_length(self, song_path):
    """Récupère la durée d'une chanson MP3"""

def update_time_label(self):
    """Met à jour l'affichage du temps en temps réel"""
```

**Système de seeking (recherche)** :
- `seek_offset_ms` : Position en millisecondes
- `ignore_end_event_until` : Ignore les faux événements de fin après un seek
- Utilise `pygame.mixer.music.play(start=position)` pour le repositionnement

#### **Gestion YouTube**

```python
def add_youtube_to_playlist(self, url=None):
    """Télécharge une vidéo YouTube et l'ajoute comme MP3"""
    # 1. Récupère les flux audio avec pytubefix
    # 2. Télécharge la vidéo
    # 3. Convertit WebM → MP3 avec moviepy
    # 4. Ajoute à la playlist
    # 5. Télécharge la pochette
```

**Processus** :
1. Extraction du meilleur flux audio avec `yt.streams.filter(only_audio=True)`
2. Téléchargement dans le dossier `musics/`
3. Conversion audio si nécessaire
4. Téléchargement de la miniature YouTube
5. Sauvegarde des métadonnées

#### **Album Art (Pochettes)**

```python
def load_album_art(self, song_path, url=None):
    """Charge la pochette depuis ID3 tags ou YouTube"""
    # Cherche d'abord dans les tags ID3 du MP3
    # Puis télécharge depuis YouTube si disponible
    # Affiche une image par défaut sinon

def set_default_album_art(self):
    """Affiche une pochette par défaut"""

def rounded_album_art(self, img, radius=20):
    """Arrondit les coins de l'image"""
```

Affiche la pochette 150×150px avec des coins arrondis et un halo de couleur.

#### **Système de Recommandations**

```python
def recommend_next_song(self):
    """Suggère une chanson basée sur l'artiste actuel"""
    # 1. Cherche d'autres chansons du même artiste
    # 2. Sinon, cherche par titre (paroles)
    # 3. Cherche par d'autres artistes de la playlist
    # 4. Propose la suivante en liste
```

- Recherche YouTube pour d'autres chansons du même artiste
- Évite les doublons
- Affiche la recommandation dans une section spéciale

#### **Métadonnées et Favoris**

```python
def save_metadata(self, path, display_title, author, ...):
    """Enregistre les métadonnées d'une chanson"""

def load_metadata(self):
    """Charge les métadonnées d'une playlist"""

def toggle_favorite(self):
    """Ajoute/enlève une chanson des favoris"""

def update_favorite_status_in_all_playlists(self, song_path, status):
    """Synchronise le statut favoris partout"""

def increment_listen_count(self, song_path):
    """Augmente le compteur d'écoutes"""
```

Chaque chanson stocke :
- `path` : Chemin du fichier
- `display_title` : Titre d'affichage
- `author` : Artiste
- `publish_date` : Date de publication
- `is_favorite` : Booléen
- `listen_count` : Nombre d'écoutes
- `url` : URL YouTube originale

#### **Thèmes et Personnalisation**

```python
def load_settings(self):
    """Charge les paramètres depuis jsons/settings.json"""

def apply_theme(self, theme_name):
    """Applique un nouveau thème à l'interface"""

def refresh_theme_ui(self):
    """Met à jour dynamiquement toutes les couleurs"""

def apply_font_scale(self, size):
    """Change la taille globale des polices (small/normal/large)"""

def open_settings(self):
    """Ouvre la fenêtre de paramètres"""
```

Les paramètres sont sauvegardés dans `jsons/settings.json` :
```json
{
    "theme": "Purple Dream",
    "volume": 0.5,
    "auto_play_next": true,
    "font_scale": "normal"
}
```

#### **Tri et Filtrage**

```python
def sort_playlist(self, option):
    """Trie la playlist selon l'option sélectionnée"""
    # - Par date d'ajout
    # - Par ordre alphabétique
    # - Par auteur
    # - Par date de création
```

#### **Recherche**

```python
def search_music(self):
    """Recherche une chanson sur YouTube et l'ajoute"""
    # 1. Demande la requête à l'utilisateur
    # 2. Cherche sur YouTube
    # 3. Ajoute le premier résultat
```

#### **Suppression**

```python
def delete_song(self):
    """Supprime une chanson de la playlist et du disque"""
    # 1. Confirme avec l'utilisateur
    # 2. Vérifie si utilisée ailleurs
    # 3. Supprime le fichier
    # 4. Met à jour les métadonnées
    # 5. Nettoie les fichiers inutilisés

def delete_playlist(self):
    """Supprime une playlist entière"""
    # Impossible pour la playlist "Favoris"

def clean_up_unused_files(self):
    """Supprime les MP3 qui ne sont plus referencés"""
```

### 5. **Serveur Web (Flask API)**

Accessible sur `http://localhost:5000` pour contrôle à distance :

#### **Routes d'État**
- `GET /status` : État actuel (titre, durée, position, volume)
- `GET /playlists` : Liste des playlists
- `GET /playlist` : Chansons de la playlist active
- `GET /search?q=query` : Recherche dans la playlist

#### **Routes de Contrôle**
- `POST /play` : Reprendre la lecture
- `POST /pause` : Pause
- `POST /next` : Chanson suivante
- `POST /prev` : Chanson précédente
- `POST /seek?pos=seconds` : Chercher à une position
- `POST /volume?level=0.5` : Définir le volume (0.0-1.0)
- `POST /play-song/<index>` : Lancer une chanson par index
- `POST /select-playlist` : Changer de playlist

#### **Routes Web**
- `GET /` : Interface web responsive
- `GET /manifest.json` : Configuration PWA
- `GET /sw.js` : Service Worker
- `GET /album-art` : Pochette actuelle
- `GET /logo.ico` : Logo de l'app

#### **Interface Web (HTML/CSS/JS)**
- Dashboard responsive mobile-friendly
- Affichage de la pochette
- Contrôles musicaux
- Liste des playlists
- Recherche de chansons
- Gestion du volume
- Compatible PWA (installable sur mobile)

### 6. **Événements et Raccourcis Clavier**

```python
self.master.bind("<space>", self.toggle_play_pause)     # Espace = Play/Pause
self.master.bind("<Right>", self.play_next_song)        # Droite = Suivant
self.master.bind("<Left>", self.play_previous_song)     # Gauche = Précédent
self.master.bind("<Escape>", ...)                       # Échap = Quitter plein écran
self.master.bind("<F11>", ...)                          # F11 = Plein écran
```

#### **Événements Pygame**
```python
def check_for_pygame_events(self):
    """Détecte la fin d'une chanson et lance la suivante"""
    # Ignore les faux événements après un seek
```

### 7. **Gestion des Fichiers**

Structure des dossiers créée automatiquement :
```
MU Player/
├── musics/           # Fichiers MP3 téléchargés
├── covers/           # Pochettes d'albums
├── jsons/
│   ├── metadata.json                    # Compatibilité
│   ├── metadata_Favoris.json            # Favoris
│   ├── metadata_[Playlist].json         # Playlists
│   ├── playlists.json                   # Liste des playlists
│   └── settings.json                    # Paramètres utilisateur
├── main.py
└── README.md
```

### 8. **Fonctions Utilitaires**

```python
def truncate_text(self, text, max_len=40):
    """Tronque le texte trop long avec '...'"""

def _hex_to_rgb(self, h):
    """Convertit couleur hex en RGB"""

def _mix(self, c1, c2, t):
    """Mélange deux couleurs (lerp)"""

def _is_light_color(self, h):
    """Détermine si une couleur est claire"""

def draw_center_gradient(self):
    """Dessine un dégradé personnalisé en arrière-plan"""
```

---

##  Fonctionnalités Principales

###  Lecture Audio
- Support MP3 natif
- Contrôle play/pause/suivant/précédent
- Barre de progression interactive (seek)
- Affichage temps réel
- Volume ajustable
- Lecture aléatoire

###  Gestion des Playlists
- Création/suppression de playlists
- Import de fichiers (liste de liens)
- Tri : date ajout, alphabétique, auteur, création
- Playlist "Favoris" par défaut
- Synchronisation métadonnées

###  YouTube
- Téléchargement automatique
- Conversion audio WebM→MP3
- Extraction de pochettes
- Recherche de chansons
- Recommandations basées artiste

###  Personnalisation
- 25 thèmes colorés
- Ajustement taille polices (3 niveaux)
- Sauvegarde des paramètres
- Interface responsive

###  Métadonnées
- Extraction ID3 tags
- Sauvegarde artiste/album/durée
- Compteur d'écoutes
- Statut favoris synchro

### Contrôle à Distance
- API web REST (Flask)
- Interface web responsive
- Compatible PWA
- Contrôle complet de la musique

---


##  Configuration et Utilisation

### Installation des dépendances
```bash
pip install -r requirements.txt
```

### Fichiers de configuration
- `jsons/settings.json` : Paramètres utilisateur
- `jsons/playlists.json` : Liste des playlists
- `jsons/metadata_*.json` : Métadonnées par playlist

### Lancement
```bash
python main.py
```

---

##  Flux de Données

```
YouTube URL
    ↓
PyTubefix (extraction flux audio)
    ↓
MoviePy (conversion WebM → MP3)
    ↓
musics/ (stockage MP3)
    ↓
Mutagen (extraction métadonnées + ID3 tags)
    ↓
jsons/metadata_[Playlist].json (sauvegarde)
    ↓
Affichage UI + Pygame (lecture audio)
```

---

##  Conclusion

Le fichier `main.py` implémente un lecteur musical complet avec une architecture bien structurée. Il combine une interface GUI riche (Tkinter), lecture audio (Pygame), gestion de fichiers JSON, téléchargement YouTube, et API web pour une expérience utilisateur complète et moderne.
