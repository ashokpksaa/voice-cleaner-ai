import os
import torch
from flask import Flask, request, send_file, send_from_directory
from flask_cors import CORS
# Direct Import logic
from df.enhance import enhance, init_df, load_audio, save_audio

app = Flask(__name__, static_folder='.')
CORS(app)

# --- AI LOAD (Global) ---
print("⏳ Loading AI Model... (Please wait)")
try:
    # Model load karte waqt config/weights download honge
    model, df_state, _ = init_df()
    print("✅ AI Model Loaded Successfully!")
except Exception as e:
    print(f"❌ Model Load Error: {e}")

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/clean-audio', methods=['POST'])
def clean_audio():
    try:
        if 'file' not in request.files:
            return "No file", 400
        
        file = request.files['file']
        
        # Files setup
        input_filename = "temp_input.wav"
        output_filename = "temp_output.wav"
        file.save(input_filename)

        print("🧠 AI Cleaning Started...")
        
        # 1. Load Audio
        audio, _ = load_audio(input_filename, sr=df_state.sr())
        
        # 2. Clean Audio (The Magic)
        enhanced_audio = enhance(model, df_state, audio)
        
        # 3. Save Audio
        save_audio(output_filename, enhanced_audio, df_state.sr())

        # 4. Send Back
        if os.path.exists(output_filename):
            print("✅ Sent Clean Audio!")
            return send_file(output_filename, mimetype="audio/wav", as_attachment=False, download_name="cleaned.wav")
        else:
            return "AI Processing Failed", 500

    except Exception as e:
        print(f"❌ Error: {e}")
        return str(e), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)