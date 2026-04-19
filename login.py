import streamlit as st
import os
from datetime import date
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega variáveis locais se houver
load_dotenv()

# Configuração do Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
STRIPE_PAYMENT_LINK = os.environ.get("STRIPE_PAYMENT_LINK", "https://MUDE_PARA_SEU_LINK_DO_STRIPE")

# Inicializando Supabase se as chaves existirem
supabase: Client | None = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        st.error(f"Erro ao conectar ao Supabase: {e}")

# estado de login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "auth_token" not in st.session_state:
    st.session_state.auth_token = None

# Função para checar a assinatura do usuário após autenticação
def checar_assinatura(email):
    if not supabase:
        st.error("Supabase não configurado.")
        return False
    
    try:
        response = supabase.table("user_subscriptions").select("*").eq("email", email).execute()
        
        if not response.data:
            # Caso não exista registro, podemos assumir desativado
            return {"status": "desativado", "data_fim": None}
        
        return response.data[0]
    except Exception as e:
        st.error(f"Erro ao buscar assinatura: {e}")
        return False

# 🔒 LOGIN / CADASTRO
if not st.session_state.logged_in:
    
    st.title("Derm AI Copilot")
    st.subheader("Faça login para continuar")

    if not supabase:
        st.warning("Aguardando configurações do Supabase nas variáveis de ambiente.")
        st.stop()

    tab1, tab2 = st.tabs(["Login", "Cadastrar"])

    with tab1:
        st.write("Digite suas credenciais")
        email_login = st.text_input("Email", key="email_l")
        senha_login = st.text_input("Senha", type="password", key="senha_l")

        if st.button("Entrar"):
            if email_login and senha_login:
                try:
                    # Autenticação via Supabase
                    auth_response = supabase.auth.sign_in_with_password({
                        "email": email_login,
                        "password": senha_login
                    })
                    
                    user_email = auth_response.user.email
                    st.session_state.user_email = user_email
                    st.session_state.auth_token = auth_response.session.access_token

                    # Verifica a assinatura
                    assinatura = checar_assinatura(user_email)
                    
                    if assinatura:
                        status = assinatura.get("status", "desativado")
                        data_fim_str = assinatura.get("data_fim")
                        
                        hoje = date.today()
                        
                        if status == "desativado":
                            st.error(f"Ative seu cadastro hoje")
                            st.markdown(f"[💳 **Clique aqui para pagar no Stripe**]({STRIPE_PAYMENT_LINK})")
                        elif status == "ativo":
                            if data_fim_str:
                                data_fim = date.fromisoformat(data_fim_str)
                                if hoje > data_fim:
                                    st.warning("Garanta mais tempo e reative seu cadastro")
                                    st.markdown(f"[💳 **Clique aqui para pagar no Stripe e renovar**]({STRIPE_PAYMENT_LINK})")
                                else:
                                    # Acesso Permitido
                                    st.success("Login efetuado com sucesso!")
                                    st.session_state.logged_in = True
                                    st.rerun()
                            else:
                                st.warning("Data de validade da assinatura não encontrada. Entre em contato com o suporte.")
                    
                except Exception as e:
                    # Pega a mensagem de erro da exception
                    st.error("Falha no login. Verifique seu email e senha.")
            else:
                st.warning("Preencha email e senha.")

    with tab2:
        st.write("Crie sua conta para utilizar o assistente")
        email_cad = st.text_input("Email", key="email_c")
        senha_cad = st.text_input("Senha", type="password", key="senha_c")
        
        if st.button("Cadastrar e Assinar"):
            if email_cad and senha_cad:
                try:
                    # 1. Cria usuário no Auth
                    res = supabase.auth.sign_up({
                        "email": email_cad,
                        "password": senha_cad
                    })
                    
                    # 2. Insere na tabela user_subscriptions
                    # Pode acontecer de o usuário já ter se cadastrado no Auth em outra tentativa, 
                    # então verificamos se já existe. Para simplificar, forçamos o insert.
                    try:
                        supabase.table("user_subscriptions").insert({
                            "email": email_cad,
                            "status": "desativado"
                        }).execute()
                    except Exception as e:
                        # Ignora se já existir
                        pass
                    
                    st.success("Conta criada com sucesso! Por favor, ative seu plano para utilizar.")
                    st.markdown(f"[💳 **Ative seu cadastro hoje pagando no Stripe**]({STRIPE_PAYMENT_LINK})")
                
                except Exception as e:
                    st.error(f"Não foi possível criar a conta: {e}")
            else:
                st.warning("Preencha email e senha.")

    st.stop()  # 🔴 impede execução do app antes do login

# ✅ APP PRINCIPAL (SEM BUG DE IMPORT)
with open("main_app.py", "r", encoding="utf-8") as f:
    code = f.read()
    exec(code, globals())