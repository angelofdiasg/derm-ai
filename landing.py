import streamlit as st

st.set_page_config(page_title="Derm AI", layout="centered")

# HERO
st.title("🧠 Derm AI")
st.subheader("Transforme consultas em prontuários completos automaticamente")

st.markdown("""
🎙️ Transcrição inteligente  
🧠 Organização médica automática  
⚡ Economia de tempo absurda  
📋 Pronto para copiar
""")

if st.button("🚀 Testar agora"):
    st.switch_page("app.py")  # seu app principal

st.divider()

# PROBLEMA
st.header("Você ainda perde tempo escrevendo tudo?")
st.markdown("""
- Consulta corrida  
- Informação se perde  
- Prontuário incompleto  
- Cansaço no final do dia  
""")

st.divider()

# SOLUÇÃO
st.header("Conheça o Derm AI")
st.markdown("""
Grave a consulta → receba:

- História clínica  
- Exame físico  
- Diagnóstico  
- Conduta  
""")

st.divider()

# COMO FUNCIONA
st.header("Como funciona")
st.markdown("""
1. Grave a consulta  
2. O Derm AI processa  
3. Receba tudo pronto  
""")

st.divider()

# CTA FINAL
st.header("Pare de perder tempo com prontuário")
if st.button("🔥 Começar agora"):
    st.switch_page("app.py")