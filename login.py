import streamlit as st
from supabase import create_client, Client

# 🔑 CONFIG SUPABASE
SUPABASE_URL = "https://mkzppjkwruvadbtzxpvz.supabase.co"
SUPABASE_KEY = "sb_publishable_jtt0pmvZxMvCMTcMwuxBgQ_asjhdW-W"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# estado de login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# tela de login
if not st.session_state.logged_in:

    st.title("Derm AI Copilot")
    st.subheader("Login")

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        # 🔓 MODO ANTIGO (fallback)
        if senha == "123456":
            st.session_state.logged_in = True
            st.rerun()

        try:
            # 🔐 login no supabase
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": senha
            })

            user = response.user

            if user is None:
                st.error("Login inválido")
            else:
                # 🔎 buscar dados do usuário
                data = supabase.table("users") \
                    .select("*") \
                    .eq("id", user.id) \
                    .execute()

                if not data.data:
                    st.error("Usuário não encontrado")
                else:
                    user_data = data.data[0]

                    # 🔒 controle de acesso
                    if not user_data.get("active_subscription", False):
                        st.error("Assinatura necessária")
                    else:
                        st.session_state.logged_in = True
                        st.rerun()

        except Exception:
            st.error("Erro ao fazer login")

# se logado abre app
if st.session_state.logged_in:

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    import main_app