import os
import torch
from flask import Flask, request, send_file, send_from_directory
from flask_cors import CORS
# DeepFilterNet ko direct import kar rahe hain (No Subprocess Error)
from df.enhance import enhance, init_df, load_audio, save_audio

app = Flask(__name__, static_folder='.')
CORS(app)

print("---------------------------------------")
print("🚀 AI SERVER: DIRECT MODEL LOADING...")
print("---------------------------------------")

# --- LOAD AI MODEL ONCE (Server Start hote hi) ---
# Isse har baar load karne ka time bachega aur Git error nahi aayega
print("⏳ Loading DeepFilterNet Model... (Wait)")
try:
    # Model, State download aur load ho jayega
    model, df_state, _ = init_df()
    print("✅ AI Model Loaded & Ready!")
except Exception as e:
    print(f"❌ Model Load Error: {e}")

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

        # 1. Save Input
        input_filename = "temp_input.wav"
        output_filename = "temp_output.wav"
        file.save(input_filename)

        # 2. RUN AI (Python Native Mode)
        print("🧠 AI Cleaning Started...")
        
        # Audio Load karo (AI ke format me)
        audio, _ = load_audio(input_filename, sr=df_state.sr())
        
        # Clean karo (Ye line asli jadu hai)
        enhanced_audio = enhance(model, df_state, audio)
        
        # Save karo
        save_audio(output_filename, enhanced_audio, df_state.sr())

        # 3. Check & Send
        if os.path.exists(output_filename):
            print("✅ Sent Cleaned Audio!")
            return send_file(output_filename, mimetype="audio/wav", as_attachment=False, download_name="cleaned_ai.wav")
        else:
            return "AI processing failed", 500

    except Exception as e:
        print(f"❌ Error: {e}")
        return str(e), 500
    
    finally:
        # Safai
        try:
            if os.path.exists("temp_input.wav"): os.remove("temp_input.wav")
            # Output hum delete nahi kar rahe taki bhej sake
        except:
            pass

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)