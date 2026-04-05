import os
from datetime import datetime


PASTA_AUDIOS = "audios_temp"


def garantir_pasta():
    if not os.path.exists(PASTA_AUDIOS):
        os.makedirs(PASTA_AUDIOS)


def salvar_audio_seguro(audio_bytes, nome_paciente):

    garantir_pasta()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    nome_arquivo = f"{nome_paciente}_{timestamp}.wav"
    caminho = os.path.join(PASTA_AUDIOS, nome_arquivo)

    with open(caminho, "wb") as f:
        f.write(audio_bytes)

    return caminho


def listar_audios():
    garantir_pasta()
    return os.listdir(PASTA_AUDIOS)