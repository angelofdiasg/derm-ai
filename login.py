import streamlit as st

# senha simples
PASSWORD = "123456"

# criar estado de login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# tela de login
if not st.session_state.logged_in:

    st.title("Derm AI Copilot")
    st.subheader("Login")

    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        if senha == PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Senha incorreta")

# se logado abre seu app
if st.session_state.logged_in:

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    exec(open("app.py").read())