import streamlit as st
from src.clinical_ai import analisar_consulta


def render_chat():

    st.divider()
    st.header("Assistente clínico (IA)")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    pergunta = st.text_input("Pergunte sobre o caso atual")

    if st.button("Enviar pergunta"):

        # -------------------------
        # CONTEXTO MULTIMODAL
        # -------------------------
        contexto = ""

        # TEXTO
        if st.session_state.transcricao_total:
            contexto += f"\nCONSULTA:\n{st.session_state.transcricao_total}\n"

        # IMAGEM
        if "imagem_resultado" in st.session_state:
            contexto += f"\nANÁLISE DA IMAGEM:\n{st.session_state.imagem_resultado}\n"

        # ABCD
        if "abcd_resultado" in st.session_state:
            contexto += "\nSCREENING MELANOMA:\n"
            contexto += f"Score: {st.session_state.abcd_resultado['score']}\n"
            contexto += f"Risco: {st.session_state.abcd_resultado['risco']}\n"

        # Se não houver nada
        if not contexto:
            st.warning("Nenhum dado clínico ou imagem disponível.")
            return

        # -------------------------
        # PROMPT
        # -------------------------
        prompt = f"""
Você é um dermatologista especialista.

Você pode receber:
- dados clínicos (consulta)
- análise de imagem
- screening de melanoma

Use TODAS as informações disponíveis.

IMPORTANTE:
- Se houver imagem, priorize análise dermatológica
- Se não houver texto, responda baseado na imagem
- NÃO repita o prontuário
- Seja direto e clínico

CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}

Responda como um especialista, em no máximo 5 linhas.
"""

        resposta = analisar_consulta(prompt)

        st.session_state.chat_history.append(("Você", pergunta))
        st.session_state.chat_history.append(("IA", resposta))

    # -------------------------
    # HISTÓRICO
    # -------------------------
    for autor, msg in st.session_state.chat_history:
        st.write(f"**{autor}:** {msg}")