from flask import Flask, request
import requests
import re
from datetime import datetime, timezone

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "COLE_O_LINK_DO_WEBHOOK_AQUI"

@app.route('/', methods=['GET', 'POST'])
def youtube_webhook():
    if request.method == 'GET':
        challenge = request.args.get('hub.challenge')
        return challenge, 200

    if request.method == 'POST':
        xml_data = request.data.decode('utf-8')
        
        # 1. Extraímos o ID do vídeo e a data de publicação (published)
        match_video = re.search(r'<yt:videoId>(.*?)</yt:videoId>', xml_data)
        match_published = re.search(r'<published>(.*?)</published>', xml_data)
        
        if match_video and match_published:
            video_id = match_video.group(1)
            published_str = match_published.group(1) # Ex: 2024-04-20T15:30:00+00:00
            
            # 2. Converte a data do vídeo para um objeto datetime
            published_time = datetime.fromisoformat(published_str.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            
            # 3. FILTRO: Só envia se o vídeo tiver menos de 60 minutos de vida
            # Isso evita que vídeos de 2 semanas atrás (reenviados pelo Google) entrem no Discord
            diferenca = (now - published_time).total_seconds()
            
            if 0 <= diferenca < 3600:
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                dados_discord = {
                    "content": f"🚨 **VÍDEO OU LIVE NOVA NA ÁREA!** 🚨\n{video_url}",
                    "username": "Radar da B.ia"
                }
                requests.post(DISCORD_WEBHOOK_URL, json=dados_discord)
            else:
                print(f"Ignorando vídeo antigo de {published_str}")

        return "OK", 200
