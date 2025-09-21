import glob
import os
import pickle
import threading
import yt_dlp
import tkinter as tk
from tkinter import ttk, messagebox
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = "token.pickle"
CLIENT_SECRETS = "client_secret.json"

def download_tiktok(url):
    ydl_opts = {"outtmpl": "downloaded.%(ext)s", "format": "mp4/best"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    matches = glob.glob("downloaded.*")
    if not matches:
        raise FileNotFoundError("Échec du téléchargement")
    return matches[0]

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)
    return creds

def upload_to_youtube(video_path, title, description, privacy):
    creds = get_credentials()
    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["tiktok"],
            "categoryId": "22"
        },
        "status": {"privacyStatus": privacy}
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
    return response.get("id")

def process():
    url = entry_url.get().strip()
    title = entry_title.get().strip()
    description = text_desc.get("1.0", tk.END).strip()
    privacy = privacy_var.get()

    if not url or not title:
        messagebox.showerror("Erreur", "URL TikTok et Titre YouTube sont requis.")
        return

    btn_start.config(state="disabled")
    status_label.config(text="Téléchargement en cours...")

    def work():
        try:
            video_file = download_tiktok(url)
            status_label.config(text="Upload en cours...")
            video_id = upload_to_youtube(video_file, title, description, privacy)
            status_label.config(text=f"✅ Upload terminé ! ID : {video_id}")
            messagebox.showinfo("Succès", f"Vidéo mise en ligne !\nID : {video_id}")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
        finally:
            btn_start.config(state="normal")

    threading.Thread(target=work).start()

# ---- Interface Tkinter ----
root = tk.Tk()
root.title("TikTok → YouTube Uploader")

frame = ttk.Frame(root, padding=10)
frame.grid()

ttk.Label(frame, text="URL TikTok :").grid(row=0, column=0, sticky="w")
entry_url = ttk.Entry(frame, width=60)
entry_url.grid(row=0, column=1, pady=5)

ttk.Label(frame, text="Titre YouTube :").grid(row=1, column=0, sticky="w")
entry_title = ttk.Entry(frame, width=60)
entry_title.grid(row=1, column=1, pady=5)

ttk.Label(frame, text="Description :").grid(row=2, column=0, sticky="nw")
text_desc = tk.Text(frame, width=60, height=5)
text_desc.grid(row=2, column=1, pady=5)

ttk.Label(frame, text="Visibilité :").grid(row=3, column=0, sticky="w")
privacy_var = tk.StringVar(value="public")
privacy_combo = ttk.Combobox(frame, textvariable=privacy_var,
                             values=["public", "unlisted", "private"], width=20)
privacy_combo.grid(row=3, column=1, pady=5, sticky="w")

btn_start = ttk.Button(frame, text="Lancer", command=process)
btn_start.grid(row=4, column=1, pady=10, sticky="e")

status_label = ttk.Label(frame, text="")
status_label.grid(row=5, column=0, columnspan=2)

root.mainloop()
