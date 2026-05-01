from flask import Flask, request
import requests
import re
from datetime import datetime, timezone

app = Flask(__name__)

# COLOQUE SEU WEBHOOK AQUI
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1499800335412236379/4_Hiz0r3U1pG_9OpAwzSMzb9f1pLKGBAK3VU4PMfZ2dcRKDXTSm5sYBI5qVn2wmY--j4"

@app.route('/', methods=['GET', 'POST'])
def youtube_webhook():
    if request.method == 'GET':
        challenge = request.args.get('hub.challenge')
        return challenge, 200

    if request.method == 'POST':
        try:
            xml_data = request.data.decode('utf-8')
            
            video_match = re.search(r'<yt:videoId>(.*?)</yt:videoId>', xml_data)
            pub_match = re.search(r'<published>(.*?)</published>', xml_data)
            
            if video_match and pub_match:
                video_id = video_match.group(1)
                pub_date_str = pub_match.group(1).replace('Z', '+00:00')
                
                # Converte para tempo real
                pub_date = datetime.fromisoformat(pub_date_str)
                agora = datetime.now(timezone.utc)
                
                # Diferença em segundos (3600s = 1 hora)
                diff = (agora - pub_date).total_seconds()
                
                # Se o vídeo tiver menos de 1 hora, manda pro Discord
                if 0 <= diff < 3600:
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    payload = {
                        "content": f"🚨 **VÍDEO NOVO NO CANAL!** 🚨\n{video_url}",
                        "username": "Radar da B.ia"
                    }
                    requests.post(DISCORD_WEBHOOK_URL, json=payload)
                
            return "OK", 200
        except Exception as e:
            print(f"Erro interno: {e}")
            return "Erro", 500 # Isso ajuda a ver o erro no log

if __name__ == "__main__":
    app.run(debug=True)
