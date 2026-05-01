from flask import Flask, request
import requests
import re
from datetime import datetime, timezone

app = Flask(__name__)

# Substitua pelo seu Webhook real
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1499800335412236379/4_Hiz0r3U1pG_9OpAwzSMzb9f1pLKGBAK3VU4PMfZ2dcRKDXTSm5sYBI5qVn2wmY--j4"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # Verificação do PubSubHubbub
        challenge = request.args.get('hub.challenge')
        if challenge:
            return challenge, 200
        return "Posto de Escuta Online! 🚛", 200

    if request.method == 'POST':
        try:
            xml_data = request.data.decode('utf-8')
            video_id = re.search(r'<yt:videoId>(.*?)</yt:videoId>', xml_data)
            pub_date_str = re.search(r'<published>(.*?)</published>', xml_data)

            if video_id and pub_date_str:
                v_id = video_id.group(1)
                # Normaliza a data para o Python entender
                p_date = datetime.fromisoformat(pub_date_str.group(1).replace('Z', '+00:00'))
                agora = datetime.now(timezone.utc)
                
                # Só dispara se o vídeo tiver menos de 1 hora (3600 segundos)
                if (agora - p_date).total_seconds() < 3600:
                    url = f"https://www.youtube.com/watch?v={v_id}"
                    requests.post(DISCORD_WEBHOOK_URL, json={
                        "content": f"🚨 **VÍDEO NOVO!** \n{url}",
                        "username": "Radar da B.ia"
                    })
            return "OK", 200
        except Exception as e:
            print(f"Erro no processamento: {e}")
            return "Erro Interno", 200 # Retornamos 200 para o Google não ficar tentando reenviar erro

# IMPORTANTE: Para a Vercel, o objeto 'app' deve estar no escopo global.
