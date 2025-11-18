from flask import Flask, render_template, request, redirect, url_for, jsonify
import os, json

app = Flask(__name__)
DATA_FILE = 'data/bai.json'
AUDIO_FOLDER = 'static/audio'

# Load dữ liệu bài học
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Save dữ liệu bài học
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', baithu=data)

@app.route('/bai/<bai_id>', methods=['GET', 'POST'])
def bai(bai_id):
    data = load_data()
    if request.method == 'POST':
        noi_dung = request.form.get('noi_dung', '')
        if bai_id not in data:
            data[bai_id] = {"tieu_de": f"Bài {bai_id}", "noi_dung": "", "audio": []}
        data[bai_id]['noi_dung'] = noi_dung
        save_data(data)
        return redirect(url_for('bai', bai_id=bai_id))
    bai_info = data.get(bai_id, {"tieu_de": f"Bài {bai_id}", "noi_dung": "", "audio": []})
    return render_template('bai.html', bai_id=bai_id, bai=bai_info)

@app.route('/upload_audio/<bai_id>', methods=['POST'])
def upload_audio(bai_id):
    if 'file' not in request.files:
        return 'No file', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    filename = file.filename
    save_path = os.path.join(AUDIO_FOLDER, filename)
    file.save(save_path)
    data = load_data()
    if bai_id not in data:
        data[bai_id] = {"tieu_de": f"Bài {bai_id}", "noi_dung": "", "audio": []}
    data[bai_id]['audio'].append({"ten": filename, "duong_dan": f"/static/audio/{filename}"})
    save_data(data)
    return redirect(url_for('bai', bai_id=bai_id))

if __name__ == '__main__':
    os.makedirs(AUDIO_FOLDER, exist_ok=True)
    os.makedirs('data', exist_ok=True)
    app.run(debug=True)
