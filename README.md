
# TikTok to YouTube Uploader

Un script Python qui permet de **télécharger vos propres vidéos TikTok** et de les **uploader automatiquement sur YouTube** avec un titre, une description et une visibilité personnalisée. Le projet inclut également une interface graphique simple pour ne pas avoir à utiliser la ligne de commande.

---

##  Fonctionnalités

- Télécharger une vidéo TikTok via son URL.
- Uploader la vidéo sur votre compte YouTube.
- Choisir le titre, la description et la visibilité (public / unlisted / private).
- Interface graphique simple avec Tkinter.
- Support des fichiers locaux et du multi-upload possible (à améliorer pour batch).

---

##  Prérequis

- Python 3.8+
- Modules Python :
  - `yt-dlp`
  - `google-api-python-client`
  - `google-auth`
  - `google-auth-oauthlib`
  - `google-auth-httplib2`
- Un compte Google avec **YouTube Data API v3** activé.
- `client_secret.json` pour OAuth2.

---

## ⚙ Installation

1. Cloner le dépôt :

```bash
git clone https://github.com/VOTRE_UTILISATEUR/tiktok-to-youtube.git
cd tiktok-to-youtube
