def interpretar_assimetria(valor):

    if valor < 10:
        return "Baixa assimetria (lesão relativamente simétrica)"
    elif valor < 25:
        return "Assimetria moderada"
    else:
        return "Assimetria elevada → achado suspeito para melanoma"


def interpretar_borda(valor):

    if valor < 0.2:
        return "Bordas regulares"
    elif valor < 0.4:
        return "Leve irregularidade de borda"
    else:
        return "Bordas muito irregulares → sugestivo de malignidade"


def interpretar_cor(valor):

    if valor < 20:
        return "Cor homogênea"
    elif valor < 50:
        return "Discreta variação de cor"
    else:
        return "Policromia importante → forte critério de suspeição"


def interpretar_diametro(valor):

    if valor < 40:
        return "Diâmetro pequeno"
    elif valor < 80:
        return "Diâmetro intermediário"
    else:
        return "Diâmetro aumentado → critério de risco (>6mm aproximado)"


def classificar_risco(score):

    if score <= 1:
        return "Baixo risco"
    elif score == 2:
        return "Risco moderado"
    else:
        return "Alto risco para melanoma"


def gerar_relatorio_clinico_abcd(abcd):

    if not abcd:
        return "Não foi possível analisar a lesão."

    explicacoes = []

    explicacoes.append(interpretar_assimetria(abcd["assimetria"]))
    explicacoes.append(interpretar_borda(abcd["irregularidade_borda"]))
    explicacoes.append(interpretar_cor(abcd["variacao_cor"]))
    explicacoes.append(interpretar_diametro(abcd["diametro_pixels"]))

    risco = classificar_risco(abcd["score"])

    # Conduta clínica
    if abcd["score"] >= 3:
        conduta = "Alta suspeita. Indicar biópsia excisional com margens."
    elif abcd["score"] == 2:
        conduta = "Avaliar com dermatoscopia. Considerar biópsia."
    else:
        conduta = "Baixa suspeita. Acompanhar clinicamente."

    return {
        "score": abcd["score"],
        "risco": risco,
        "explicacoes": explicacoes,
        "conduta": conduta
    }