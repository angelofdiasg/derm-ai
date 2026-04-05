from openai import OpenAI
import os
from dotenv import load_dotenv
import time

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcrever_audio(caminho_audio, tentativas=3):

    for tentativa in range(tentativas):
        try:
            with open(caminho_audio, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )

            return transcript.text

        except Exception as e:
            print(f"Erro tentativa {tentativa+1}: {e}")
            time.sleep(2)

    raise Exception("Falha ao transcrever após várias tentativas")