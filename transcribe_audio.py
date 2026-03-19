from openai import OpenAI
from dotenv import load_dotenv
import os
from pydub import AudioSegment

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MAX_SIZE = 24 * 1024 * 1024  # 24 MB


def dividir_audio(audio_path):

    audio = AudioSegment.from_file(audio_path)

    duracao_parte = 5 * 60 * 1000  # 5 minutos

    partes = []

    for i in range(0, len(audio), duracao_parte):

        parte = audio[i:i + duracao_parte]

        nome = f"{audio_path}_parte_{i}.mp3"

        parte.export(nome, format="mp3")

        partes.append(nome)

    return partes


def transcrever_audio(audio_path):

    tamanho = os.path.getsize(audio_path)

    texto_final = ""

    # Se áudio menor que limite
    if tamanho < MAX_SIZE:

        with open(audio_path, "rb") as audio_file:

            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        return transcript.text

    # Se áudio grande → dividir
    partes = dividir_audio(audio_path)

    for parte in partes:

        with open(parte, "rb") as audio_file:

            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        texto_final += transcript.text + "\n"

    return texto_final