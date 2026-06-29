import streamlit as st
from buscador import rodar_busca_geral

st.set_page_config(page_title="Plataforma de Viagens Inteligente", page_icon="✈️", layout="wide")

st.markdown("""
<style>
    .cartao-info {
        background-color: #ffffff !important;
        color: #212529 !important;
        padding: 22px;
        border-radius: 12px;
        border-left: 6px solid #007AFF;
        margin-bottom: 20px;
        box-shadow: 0px 4px 14px rgba(0, 0, 0, 0.05);
    }
    .titulo-cartao { color: #007AFF; font-weight: bold; font-size: 18px; margin-bottom: 8px; }
    .header-resultado { font-size: 28px; font-weight: bold; color: #1C1C1E; }
    .caixa-abnt {
        background-color: #f8f9fa !important;
        border: 1px solid #ced4da !important;
        padding: 40px !important;
        font-family: 'Times New Roman', Times, serif !important;
        color: #000000 !important;
        line-height: 1.6 !important;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=300&q=80", use_column_width=True)
    st.markdown("### 🔍 Configuração do Planejamento")

    destino_usuario = st.text_input("📍 Digite o destino (Cidade/Estado/País):", value="Canadá")
    mes_usuario = st.selectbox(
        "📅 Mês de Foco Inicial:",
        ["Independente do mês", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
         "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    )

    botao_pesquisar = st.button("🔎 Atualizar Listagem", use_container_width=True, type="primary")

st.title("✈️ Portal de Inteligência Turística Local")
st.write("Consolide relatórios geográficos, cenários visuais exclusivos, fuso horário e tabelas climatológicas.")

if 'dados_site' not in st.session_state:
    st.session_state['last_dest'] = destino_usuario
    st.session_state['last_month'] = mes_usuario
    with st.spinner(f"Inicializando dados automáticos para {destino_usuario}..."):
        retorno_inicial = rodar_busca_geral(destino_usuario, mes_usuario)
        if retorno_inicial:
            st.session_state['dados_site'] = retorno_inicial

if botao_pesquisar or (destino_usuario and st.session_state.get('last_dest') != destino_usuario) or (mes_usuario and st.session_state.get('last_month') != mes_usuario):
    st.session_state['last_dest'] = destino_usuario
    st.session_state['last_month'] = mes_usuario

    with st.spinner(f"Processando novas informações para {destino_usuario}..."):
        retorno_api = rodar_busca_geral(destino_usuario, mes_usuario)
        if retorno_api:
            st.session_state['dados_site'] = retorno_api

if 'dados_site' in st.session_state:
    dados = st.session_state['dados_site']

    st.markdown("---")
    st.markdown(f"<div class='header-resultado'>🗺️ Destino Analisado: {dados['destino']}</div>", unsafe_allow_html=True)
    st.caption(f"🗓️ Período de Referência em Análise: **{dados['mes_planejado']}**")

    col_esquerda, col_direita = st.columns([1.2, 1])

    with col_esquerda:
        st.image(dados['imagem_capa'], caption=f"Região de Destaque Turístico em {dados['destino']}", use_container_width=True)

    with col_direita:
        st.markdown(f"""
        <div class='cartao-info'>
            <div class='titulo-cartao'>🏛️ Localização Geográfica e Pontos Turísticos Principais</div>
            <p><b>Estados, Cidades e Atrações Mapeadas:</b><br>{dados['resumo']}</p>
            <hr>
            <p><b>🕐 Sistema de Fusos Horários (Ref. Horário de Brasília):</b><br>{dados['fuso_horario']}</p>
            <hr>
            <p><b>💱 Cotação da Moeda Local (Compra):</b><br>{dados['valor_moeda_compra']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📊 Indicadores Meteorológicos Médios e Sazonalidade (Mês a Mês)")
    st.write("Abaixo está a listagem anual contendo as flutuações das médias de temperatura para o planejamento de desembarque:")
    st.table(dados['tabela_valores'])

    st.markdown("---")
    st.markdown("### 📄 Arquivo de Documentação Técnica Gerado")

    linhas_tabela_html = ""
    for item in dados['tabela_valores']:
        linhas_tabela_html += f"""
        <tr>
            <td style='border: 1px solid #ddd; padding: 6px;'>{item['Mês']}</td>
            <td style='border: 1px solid #ddd; padding: 6px; text-align: center;'>{item['Temperatura Média']}</td>
            <td style='border: 1px solid #ddd; padding: 6px;'>{item['Sazonalidade']}</td>
            <td style='border: 1px solid #ddd; padding: 6px;'>{item['Condição Operacional']}</td>
        </tr>
        """

    texto_abnt = f"""
    <div class='caixa-abnt'>
        <p style='text-align: center; font-weight: bold; text-transform: uppercase;'>UNIVERSIDADE GLOBAL DE TECNOLOGIA E TURISMO<br>SISTEMA DE MONITORAMENTO DE MERCADO E DIRETRIZES DE VIAGEM</p>
        <br>
        <p style='text-align: center; font-weight: bold; font-size: 18px; text-transform: uppercase;'>RELATÓRIO TÉCNICO DE VIAGEM E MAPEAMENTO CLIMÁTICO: {dados['destino'].upper()}</p>
        <br>
        <p style='text-align: justify;'><b>1. CONFIGURAÇÃO GEOGRÁFICA, ESTADOS E PONTOS TURÍSTICOS</b><br>
        Este documento consolida o mapeamento macrogeográfico realizado para o destino {dados['destino']}. O levantamento de dados identificou os eixos estaduais e municipais de maior fluxo turístico, registrando a seguinte consolidação estrutural das atrações mais visitadas da região: {dados['resumo']}.</p>

        <p style='text-align: justify;'><b>2. SINCROLOGIA INTERNACIONAL E MARCADORES DE FUSO HORÁRIO</b><br>
        Para fins de alinhamento de infraestrutura de transporte e comunicações corporativas, determinou-se que o fuso horário oficial associado ao destino apresenta-se configurado como: <u>{dados['fuso_horario']}</u>, tendo como vetor referencial a hora oficial de Brasília (GMT-3).</p>

        <p style='text-align: justify;'><b>3. COMPORTAMENTO METEOROLÓGICO ANUAL E TEMPERATURAS MÉDIAS</b><br>
        Abaixo apresenta-se a distribuição sistemática dos doze meses cronológicos do ano, discriminando as médias térmicas estimadas e as respectivas janelas de sazonalidade comercial do mercado de turismo:</p>

        <table style='width: 100%; border-collapse: collapse; font-family: Arial, sans-serif; font-size: 13px; margin: 15px 0;'>
            <thead>
                <tr style='background-color: #f2f2f2; font-weight: bold;'>
                    <th style='border: 1px solid #ddd; padding: 8px; text-align: left;'>Mês Cronológico</th>
                    <th style='border: 1px solid #ddd; padding: 8px; text-align: center;'>Temperatura Média</th>
                    <th style='border: 1px solid #ddd; padding: 8px; text-align: left;'>Sazonalidade Comercial</th>
                    <th style='border: 1px solid #ddd; padding: 8px; text-align: left;'>Condição Climática Observada</th>
                </tr>
            </thead>
            <tbody>
                {linhas_tabela_html}
            </tbody>
        </table>

        <p style='text-align: justify;'><b>4. DIRETRIZES LOGÍSTICAS E DIRECIONAMENTO ALFANDEGÁRIO</b><br>
        Com base nos indexadores financeiros oficiais e na coleta mercantil de câmbio, estipulou-se o valor de compra em tempo real de <b>{dados['valor_moeda_compra']}</b> por unidade de moeda nacional, balizando os limites de declaração de fundos exigidos pelos órgãos competentes.</p>
        <br><br>
        <p style='text-align: center;'>Mapeamento Governamental e Comercial de Dados — Ano 2026</p>
    </div>
    """
    st.markdown(texto_abnt, unsafe_allow_html=True)
