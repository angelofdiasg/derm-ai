from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analisar_consulta(texto):

    prompt = f"""
Você é um dermatologista experiente.

Analise a consulta abaixo e produza um PRONTUÁRIO DERMATOLÓGICO DETALHADO.

Regras:

- Use linguagem médica
- Não resuma excessivamente
- Estruture o texto claramente
- Não escreva "não informado"
- Se alguma informação não estiver presente simplesmente omita

Estrutura desejada:

1. História clínica
Descreva início da lesão, evolução, sintomas associados, fatores desencadeantes.

2. Exame dermatológico
Descreva morfologia, cor, superfície, bordas, localização anatômica.

3. Diagnósticos diferenciais
Liste diagnósticos possíveis em dermatologia.

4. Diagnóstico mais provável
Explique brevemente.

5. CID provável
Informe o CID-10 compatível.

6. Conduta sugerida
Inclua investigação, tratamento ou necessidade de biópsia.

Consulta:

{texto}
"""

    resposta = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return resposta.choices[0].message.content