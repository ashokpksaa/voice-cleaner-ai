import os
import subprocess
import shutil
from flask import Flask, request, send_file, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)

print("---------------------------------------")
print("🚀 AI SERVER: PURE DEEPFILTERNET (BEST)...")
print("---------------------------------------")

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/clean-audio', methods=['POST'])
def clean_audio():
    try:
        if 'file' not in request.files:
            return "No file part", 400
        
        file = request.files['file']
        print("🎤 Audio Received...")

        # 1. Clean old files first (Safety cleanup)
        for f in os.listdir('.'):
            if f.startswith("temp_") or f.endswith("_DeepFilterNet3.wav"):
                try: os.remove(f)
                except: pass

        # 2. Save New File
        input_filename = "temp_input.wav"
        file.save(input_filename)

        # 3. RUN AI (No Extra Math, Just Brain)
        print("🧠 AI Cleaning...")
        
        # DeepFilterNet default settings are the best (Krisp logic)
        process = subprocess.run(
            ["deepFilter", input_filename], 
            capture_output=True, 
            text=True
        )

        if process.returncode != 0:
            print("❌ AI Error:", process.stderr)
            return f"AI Error: {process.stderr}", 500

        # 4. Find Output
        # DFNet auto-names it: temp_input_DeepFilterNet3.wav
        expected_output = "temp_input_DeepFilterNet3.wav"

        if os.path.exists(expected_output):
            print("✅ Sent Pure AI Audio!")
            return send_file(expected_output, mimetype="audio/wav", as_attachment=False, download_name="cleaned_final.wav")
        else:
            return "Output file missing", 500

    except Exception as e:
        print(f"❌ Error: {e}")
        return str(e), 500

if __name__ == '__main__':
    # Cloud ka port lega, nahi mila to 10000 use karega
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)