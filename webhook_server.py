import os
import stripe
from fastapi import FastAPI, Request, Header, HTTPException
from supabase import create_client, Client
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()

# Configuração do Stripe
stripe.api_key = os.environ.get("STRIPE_API_KEY")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")

# Configuração do Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client | None = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Stripe Webhook Server")

@app.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="STRIPE_WEBHOOK_SECRET não configurado")
    
    payload = await request.body()
    
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Payload inválido
        raise HTTPException(status_code=400, detail="Payload inválido")
    except stripe.error.SignatureVerificationError as e:
        # Assinatura inválida
        raise HTTPException(status_code=400, detail="Assinatura inválida")

    # Trata os eventos
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Pega o email do cliente de forma garantida contra objetos limitados do SDK
        email = None
        try:
            cd = session.get('customer_details')
            if cd:
                if hasattr(cd, 'email'):
                    email = cd.email
                elif 'email' in cd:
                    email = cd['email']
        except Exception:
            pass
            
        if not email:
            email = session.get('customer_email')
            
        if email and supabase:
            atualizar_assinatura(email)
            print(f"Assinatura atualizada para o email: {email}")
        else:
            print("Email não encontrado no payload do Stripe ou Supabase não configurado.")
            
    elif event['type'] == 'invoice.payment_succeeded':
        # Também pode ser usado para renovações automáticas
        invoice = event['data']['object']
        email = invoice.get('customer_email')
        if email and supabase:
            atualizar_assinatura(email)
            print(f"Renovação efetuada para o email: {email}")

    return {"status": "success"}

def atualizar_assinatura(email: str):
    """
    Se estiver desativado -> muda para ativo, data_inicio hoje, data_fim = hoje + 365 dias
    Se estiver ativo -> só adiciona 365 dias na data_fim
    """
    try:
        response = supabase.table("user_subscriptions").select("*").eq("email", email).execute()
        
        hoje = date.today()
        um_ano = timedelta(days=365)
        
        if response.data and len(response.data) > 0:
            reg = response.data[0]
            status_atual = reg.get("status")
            data_fim_str = reg.get("data_fim")
            
            nova_data_fim = hoje + um_ano
            novo_status = "ativo"
            nova_data_inicio = hoje
            
            if status_atual == "ativo" and data_fim_str:
                data_fim_atual = date.fromisoformat(data_fim_str)
                # Se ainda tem tempo sobrando, soma a partir de hoje ou do fim? 
                # Conforme regra, muda apenas o período estendendo
                nova_data_fim = data_fim_atual + um_ano
                # data inicio continua a mesma, então não atualizar
                supabase.table("user_subscriptions").update({
                    "data_fim": nova_data_fim.isoformat()
                }).eq("email", email).execute()
                
            else:
                # Estava desativado ou sem data
                supabase.table("user_subscriptions").update({
                    "status": novo_status,
                    "data_inicio": nova_data_inicio.isoformat(),
                    "data_fim": nova_data_fim.isoformat()
                }).eq("email", email).execute()
        else:
            # Caso não exista registro, criamos um novo já ativo
            supabase.table("user_subscriptions").insert({
                "email": email,
                "status": "ativo",
                "data_inicio": hoje.isoformat(),
                "data_fim": (hoje + um_ano).isoformat()
            }).execute()
            
    except Exception as e:
        print(f"Erro ao atualizar o Supabase para {email}: {e}")

# Para rodar manualmente: uvicorn webhook_server:app --host 0.0.0.0 --port 8000
