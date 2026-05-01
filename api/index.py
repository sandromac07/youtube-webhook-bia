from flask import Flask, request
import requests
import re
from datetime import datetime, timezone

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1499800335412236379/4_Hiz0r3U1pG_9OpAwzSMzb9f1pLKGBAK3VU4PMfZ2dcRKDXTSm5sYBI5qVn2wmY--j4"

# Memória temporária para evitar duplicatas no mesmo ciclo de execução
processados = []

@app.route('/', methods=['GET', 'POST'])
def youtube_webhook():
    global processados
    
    if request.method == 'GET':
        challenge = request.args.get('hub.challenge')
        return challenge if challenge else "Posto Online! 🚛", 200

    if request.method == 'POST':
        try:
            xml_data = request.data.decode('utf-8')
            video_id_match = re.search(r'<yt:videoId>(.*?)</yt:videoId>', xml_data)
            pub_match = re.search(r'<published>(.*?)</published>', xml_data)

            if video_id_match and pub_match:
                v_id = video_id_match.group(1)
                p_date_str = pub_match.group(1).replace('Z', '+00:00')
                p_date = datetime.fromisoformat(p_date_str)
                agora = datetime.now(timezone.utc)

                # 1. Filtro de Tempo mais rígido (apenas vídeos com menos de 10 minutos)
                # Isso mata os vídeos de 2 semanas atrás de vez.
                if (agora - p_date).total_seconds() < 600:
                    
                    # 2. Filtro de ID (Se já processou esse ID agora, ignora)
                    if v_id not in processados:
                        url = f"https://www.youtube.com/watch?v={v_id}"
                        
                        requests.post(DISCORD_WEBHOOK_URL, json={
                            "content": f"🚨 **VÍDEO NOVO!** \n{url}",
                            "username": "Radar da B.ia"
                        })
                        
                        # Adiciona à lista e mantém apenas os últimos 10 IDs para não encher a memória
                        processados.append(v_id)
                        processados = processados[-10:]
            
            return "OK", 200
        except Exception as e:
            return f"Erro: {e}", 200 # Retorna 200 para o Google não reenviar o erro
