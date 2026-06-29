import urllib.parse
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st

try:
    EMAIL_SUPORTE = st.secrets.get("EMAIL_SUPORTE", "automacao.teste.2026@outlook.com")
    SENHA_SUPORTE = st.secrets.get("SENHA_SUPORTE", "@Daniel2022")
except Exception:
    EMAIL_SUPORTE = "automacao.teste.2026@outlook.com"
    SENHA_SUPORTE = "@Daniel2022"


def notificar_problema_sistema(detalhes_erro):
    smtp_server = "smtp.office365.com"
    porto_smtp = 587
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SUPORTE
    msg['To'] = EMAIL_SUPORTE
    msg['Subject'] = "🚨 ALERTA: Erro Crítico na Inicialização de Dados de Viagem"
    corpo = f"Falha reportada na geração de relatórios:\n\n{detalhes_erro}"
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        servidor = smtplib.SMTP(smtp_server, porto_smtp, timeout=5)
        servidor.ehlo()
        servidor.starttls()
        servidor.ehlo()
        servidor.login(EMAIL_SUPORTE, SENHA_SUPORTE)
        servidor.sendmail(EMAIL_SUPORTE, EMAIL_SUPORTE, msg.as_string())
        servidor.quit()
    except Exception as e:
        print(f"Não foi possível notificar o suporte via SMTP (Bloqueio de nuvem ou credenciais): {e}")


def buscar_imagem_postal_exata(destino):
    destino_busca = destino.strip().lower()
    mapa_postais = {
        "brasil": "https://images.unsplash.com/photo-1516306580629-468a6e7de10d?auto=format&fit=crop&w=1200&q=80",
        "frança": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=1200&q=80",
        "canadá": "https://images.unsplash.com/photo-1487621167305-5d248087c724?auto=format&fit=crop&w=1200&q=80",
        "canada": "https://images.unsplash.com/photo-1487621167305-5d248087c724?auto=format&fit=crop&w=1200&q=80",
        "japão": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=1200&q=80",
        "estados unidos": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&w=1200&q=80"
    }
    if destino_busca in mapa_postais:
        return mapa_postais[destino_busca]
    termo_ingles = urllib.parse.quote(f"{destino_busca} landmark famous tourism")
    return f"https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80&sig={termo_ingles}"


def buscar_fuso_horario(destino):
    cabeçalho = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    termo = f"fuso horario de {destino} em relacao ao brasil brasilia"
    url = f"https://www.google.com/search?q={urllib.parse.quote(termo)}"
    try:
        resposta = requests.get(url, headers=cabeçalho, timeout=5)
        if resposta.status_code == 200:
            sopa = BeautifulSoup(resposta.text, 'html.parser')
            bloco = sopa.select_one("div.BNeawe")
            if bloco:
                return bloco.text.strip()
    except Exception as e:
        notificar_problema_sistema(f"Fuso horário indisponível via scraping: {e}")
    return "Fuso horário variável conforme o Estado selecionado"


def buscar_cotacao_moeda(destino):
    cabeçalho = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    termo = f"qual a moeda oficial de {destino} e valor em real para compra hoje"
    url = f"https://www.google.com/search?q={urllib.parse.quote(termo)}"
    try:
        resposta = requests.get(url, headers=cabeçalho, timeout=5)
        if resposta.status_code == 200:
            sopa = BeautifulSoup(resposta.text, 'html.parser')
            bloco = sopa.select_one("span.DFlfde, div.BNeawe")
            if bloco:
                return bloco.text.strip()
    except Exception:
        pass
    return "5.45 (Valor Comercial Estimado)"


def buscar_ponto_turistico_completo(destino):
    cabeçalho = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Accept-Language": "pt-BR,pt;q=0.9"}
    termo = f"principais pontos turisticos estados e cidades mais visitados de {destino}"
    url = f"https://www.google.com/search?q={urllib.parse.quote(termo)}"
    try:
        resposta = requests.get(url, headers=cabeçalho, timeout=5)
        if resposta.status_code == 200:
            sopa = BeautifulSoup(resposta.text, 'html.parser')
            snippets = sopa.select("div.VwiC3b, div.BNeawe")
            textos = [el.text.strip() for el in snippets if len(el.text.strip()) > 50]
            if textos:
                return textos[0]
    except Exception:
        pass
    return f"Mapeamento multirregional focado nos principais eixos econômicos e históricos de {destino}."


def gerar_calendario_temperaturas(destino):
    destino_ajustado = destino.lower().strip()
    if "canadá" in destino_ajustado or "canada" in destino_ajustado:
        temps = [-10, -8, -2, 6, 13, 18, 22, 21, 16, 9, 2, -5]
    elif "frança" in destino_ajustado or "franca" in destino_ajustado:
        temps = [5, 6, 9, 12, 16, 20, 23, 22, 19, 14, 9, 6]
    elif "japão" in destino_ajustado or "japao" in destino_ajustado:
        temps = [5, 6, 9, 14, 19, 22, 26, 27, 23, 18, 12, 7]
    elif "estados unidos" in destino_ajustado or "usa" in destino_ajustado or "eua" in destino_ajustado:
        temps = [2, 4, 9, 15, 20, 25, 28, 27, 23, 16, 10, 4]
    else:
        temps = [26, 27, 26, 24, 22, 20, 20, 21, 23, 24, 25, 26]

    meses_nomes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                   "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    tabela_clima = []
    for i, nome_mes in enumerate(meses_nomes):
        t = temps[i]
        if nome_mes in ["Dezembro", "Janeiro", "Fevereiro", "Julho"]:
            sazonalidade = "🚀 Alta Temporada"
            condicao = "Fluxo Máximo / Clima Extremo" if t < 5 else "Fluxo Máximo / Verão Dinâmico"
        elif nome_mes in ["Junho", "Agosto", "Novembro"]:
            sazonalidade = "📉 Baixa Temporada"
            condicao = "Período Chuvoso / Instável" if t > 15 else "Frio Intenso / Baixo Fluxo"
        else:
            sazonalidade = "⚖️ Média Temporada"
            condicao = "Clima Ameno / Condições Ideais"

        tabela_clima.append({
            "Mês": nome_mes,
            "Temperatura Média": f"{t}°C",
            "Sazonalidade": sazonalidade,
            "Condição Operacional": condicao
        })
    return tabela_clima


def rodar_busca_geral(destino, mes):
    destino_limpo = destino.strip().title()
    try:
        foto_unica = buscar_imagem_postal_exata(destino_limpo)
        resumo_geografico = buscar_ponto_turistico_completo(destino_limpo)
        valor_cambio = buscar_cotacao_moeda(destino_limpo)
        fuso_local = buscar_fuso_horario(destino_limpo)
        cronograma_clima = gerar_calendario_temperaturas(destino_limpo)

        return {
            "destino": destino_limpo,
            "mes_planejado": mes,
            "imagem_capa": foto_unica,
            "resumo": resumo_geografico,
            "fuso_horario": fuso_local,
            "valor_moeda_compra": valor_cambio,
            "tabela_valores": cronograma_clima,
            "hoteis": ["Rede hoteleira centralizada por state", "Estadias Executivas Locais"],
            "restaurantes": ["Gastronomia Tradicional Regional", "Centros Gastronômicos Urbanos"]
        }
    except Exception as erro:
        notificar_problema_sistema(f"Erro ao processar mapeamento para {destino_limpo}: {erro}")
        return None
