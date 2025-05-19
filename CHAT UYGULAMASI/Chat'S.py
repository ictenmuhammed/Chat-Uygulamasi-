from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)

# Mesaj geçmişi log dosyasının yolu
LOG_FILE = 'message_log.txt'

# Kullanıcıları tutan set
users = set()

# Ana sayfa
@app.route('/')
def index():
    return render_template('index.html')

# WebSocket üzerinden mesaj alma ve gönderme
@socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Mesajı log dosyasına kaydetme
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"{timestamp} - {username}: {message}\n")
    
    # Mesajı yayınla (diğer kullanıcılara ilet)
    emit('response', {'username': username, 'message': message, 'timestamp': timestamp}, broadcast=True)

# Yeni bir kullanıcı sohbete katıldığında bu fonksiyon çalışacak
@socketio.on('user_joined')
def handle_user_joined(data):
    username = data['username']
    
    # Kullanıcıyı kullanıcılar listesine ekle
    users.add(username)
    
    # Katılım mesajı gönder
    message = f"{username} katıldı."
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Mesajı log dosyasına kaydetme
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"{timestamp} - ADMIN: {message}\n")

    # Katılım mesajını tüm kullanıcılara gönder
    emit('response', {'username': 'ADMIN', 'message': message, 'timestamp': timestamp}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
