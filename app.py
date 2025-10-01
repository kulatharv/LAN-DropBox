from flask import Flask, render_template, request, jsonify, send_file
import os, qrcode, json, socket
from io import BytesIO
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
LOG_FILE = 'upload_log.json'
DEVICES_FILE = 'devices.json'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
if not os.path.exists(LOG_FILE): json.dump([], open(LOG_FILE,'w'))
if not os.path.exists(DEVICES_FILE): json.dump([], open(DEVICES_FILE,'w'))

def log_upload(filename, ip):
    logs = json.load(open(LOG_FILE,'r'))
    logs.append({"filename": filename, "timestamp": str(datetime.now()), "device": ip})
    json.dump(logs, open(LOG_FILE,'w'))

def add_device(ip):
    devices = json.load(open(DEVICES_FILE,'r'))
    if ip not in [d['ip'] for d in devices]:
        devices.append({"ip": ip, "timestamp": str(datetime.now())})
    json.dump(devices, open(DEVICES_FILE,'w'))

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8",80))
        ip = s.getsockname()[0]
    except:
        ip="127.0.0.1"
    finally:
        s.close()
    return ip

@app.route('/')
def dashboard():
    local_ip = get_local_ip()
    device_ip = request.remote_addr       # get the visitor's IP
    add_device(device_ip)                 # add/update device in JSON
    devices = json.load(open(DEVICES_FILE,'r'))
    return render_template('dashboard.html', local_ip=local_ip, devices=devices)

@app.route('/files')
def files_page():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('files.html', files=files)

@app.route('/logs')
def logs_page():
    logs = json.load(open(LOG_FILE,'r'))
    return render_template('logs.html', logs=logs)

@app.route('/upload', methods=['POST'])
def upload_file():
    ip = request.remote_addr
    add_device(ip)
    if 'file' not in request.files: return jsonify({"error":"No file"}),400
    file = request.files['file']
    if file.filename == '': return jsonify({"error":"No selected file"}),400
    path = os.path.join(UPLOAD_FOLDER,file.filename)
    file.save(path)
    log_upload(file.filename, ip)
    return jsonify({"success":True, "filename":file.filename})

@app.route('/get_qr/<filename>')
def get_qr(filename):
    path = os.path.join(UPLOAD_FOLDER,filename)
    if not os.path.exists(path): return jsonify({"error":"File not found"}),404
    qr = qrcode.QRCode(version=1, box_size=6, border=3)
    qr.add_data(os.path.abspath(path))
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/get_dashboard_qr')
def dashboard_qr():
    local_ip = get_local_ip()
    url = f"http://{local_ip}:5000/"
    qr = qrcode.QRCode(version=1, box_size=6, border=3)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
        logs = json.load(open(LOG_FILE,'r'))
        logs = [l for l in logs if l['filename']!=filename]
        json.dump(logs, open(LOG_FILE,'w'))
        return jsonify({"success":True})
    return jsonify({"error":"File not found"}),404

@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path): return send_file(path, as_attachment=True)
    return "File not found",404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
