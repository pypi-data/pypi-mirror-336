from gtts import gTTS
import os

def text_to_audio(text, lang='en', output_file='output.mp3'):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_file)
        print(f"Audio saved as {output_file}")
        # Optional: Play the audio
        os.system(f"start {output_file}" if os.name == "nt" else f"mpg321 {output_file}")
    except Exception as e:
        print(f"Error: {e}")