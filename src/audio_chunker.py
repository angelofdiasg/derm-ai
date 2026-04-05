import os
from pydub import AudioSegment
import tempfile

MAX_SIZE_MB = 20


def dividir_audio(caminho_audio):

    audio = AudioSegment.from_file(caminho_audio)

    tamanho_bytes = os.path.getsize(caminho_audio)
    tamanho_mb = tamanho_bytes / (1024 * 1024)

    if tamanho_mb <= MAX_SIZE_MB:
        return [caminho_audio]

    partes = []
    duracao_total = len(audio)

    num_partes = int(tamanho_mb // MAX_SIZE_MB) + 1
    duracao_por_parte = duracao_total / num_partes

    for i in range(num_partes):

        inicio = int(i * duracao_por_parte)
        fim = int((i + 1) * duracao_por_parte)

        chunk = audio[inicio:fim]

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        chunk.export(temp_file.name, format="mp3", bitrate="128k")

        partes.append(temp_file.name)

    return partes


def transcrever_audio_grande(caminho_audio, transcrever_func, progress_bar=None):

    partes = dividir_audio(caminho_audio)

    texto_final = ""

    total = len(partes)

    for i, parte in enumerate(partes):
        texto = transcrever_func(parte)
        texto_final += "\n" + texto

        # atualizar barra de progresso
        if progress_bar:
            progress_bar.progress((i + 1) / total)

        # remover arquivo temporário
        if parte != caminho_audio:
            os.remove(parte)

    return texto_final.strip()