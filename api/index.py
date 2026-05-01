from flask import Flask, request
import requests
import re

app = Flask(__name__)

# COLE AQUI O LINK DO SEU WEBHOOK DO DISCORD (Aquele que criamos lá no começo)
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1499800335412236379/4_Hiz0r3U1pG_9OpAwzSMzb9f1pLKGBAK3VU4PMfZ2dcRKDXTSm5sYBI5qVn2wmY--j4"

@app.route('/', methods=['GET', 'POST'])
def youtube_webhook():
    # 1. A VERIFICAÇÃO DO GOOGLE (O "Aperto de Mão")
    # Quando você cadastra o canal, o Google manda um código por GET para ver se o servidor é seu.
    if request.method == 'GET':
        challenge = request.args.get('hub.challenge')
        if challenge:
            return challenge, 200
        return "Posto de Escuta da Firma está Online! 🚛", 200

    # 2. O AVISO DE VÍDEO NOVO (O "Grito" do YouTube)
    # Quando sai vídeo/live, o Google manda um POST com um arquivo de texto (XML).
    if request.method == 'POST':
        xml_data = request.data.decode('utf-8')
        
        # Procuramos o ID do vídeo no meio do texto que o Google mandou
        match_video = re.search(r'<yt:videoId>(.*?)</yt:videoId>', xml_data)
        
        if match_video:
            video_id = match_video.group(1)
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            # Monta a mensagem que vai para o Discord
            dados_discord = {
                "content": f"🚨 **VÍDEO OU LIVE NOVA NA ÁREA!** 🚨\n{video_url}",
                "username": "Radar da B.ia", # Nome que vai aparecer no Webhook
                "avatar_url": "https://i.imgur.com/8nLFCVP.png" # Foto opcional
            }
            
            # Dispara para o Discord instantaneamente!
            requests.post(DISCORD_WEBHOOK_URL, json=dados_discord)
            
        return "OK", 200

# Necessário para o Vercel entender onde o app começa
if __name__ == '__main__':
    app.run(port=5000)