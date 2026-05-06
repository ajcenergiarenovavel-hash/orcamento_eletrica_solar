import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Gerador de Orçamentos - Energia", layout="wide")

st.title("⚡ Gerador de Orçamentos: Elétrica & Solar")
st.markdown("---")

# 1. Carregamento de Dados
@st.cache_data
def carregar_dados():
    # Simulando a leitura de abas da planilha
    # df_materiais = pd.read_excel("precos.xlsx", sheet_name="Materiais")
    data = {
        "Item": ["Inversor 5kW", "Painel 550W", "Cabo Solar 6mm", "Disjuntor DIN"],
        "Preço Unitário": [4500.00, 850.00, 12.50, 45.00],
        "Categoria": ["Solar", "Solar", "Elétrica", "Elétrica"]
    }
    return pd.DataFrame(data)

df_precos = carregar_dados()

# 2. Interface de Entrada
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Dados do Cliente")
    nome_cliente = st.text_input("Nome do Cliente")
    tipo_servico = st.selectbox("Tipo de Serviço", ["Solar Fotovoltaico", "Instalação Elétrica", "Híbrido"])

with col2:
    st.subheader("🏗️ Dimensionamento")
    if tipo_servico == "Solar Fotovoltaico" or tipo_servico == "Híbrido":
        potencia = st.number_input("Potência do Sistema (kWp)", min_value=0.0, step=0.1)
    mao_de_obra = st.number_input("Valor da Mão de Obra (R$)", min_value=0.0)

# 3. Seleção de Itens da Planilha
st.subheader("🛒 Materiais e Equipamentos")
itens_selecionados = st.multiselect("Selecione os itens necessários:", df_precos["Item"].unique())

lista_orcamento = []
if itens_selecionados:
    for item in itens_selecionados:
        preco_unit = df_precos.loc[df_precos["Item"] == item, "Preço Unitário"].values[0]
        qtd = st.number_input(f"Quantidade para {item}", min_value=1, key=item)
        lista_orcamento.append({"Item": item, "Qtd": qtd, "Preço Unit.": preco_unit, "Total": qtd * preco_unit})

# 4. Cálculo e Resumo
if st.button("Gerar Orçamento Final"):
    df_final = pd.DataFrame(lista_orcamento)
    total_materiais = df_final["Total"].sum()
    valor_final = total_materiais + mao_de_obra

    st.markdown("---")
    st.header(f"Resumo do Orçamento: {nome_cliente}")
    st.table(df_final)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Materiais", f"R$ {total_materiais:,.2f}")
    c2.metric("Mão de Obra", f"R$ {mao_de_obra:,.2f}")
    c3.metric("VALOR TOTAL", f"R$ {valor_final:,.2f}")

    # Botão para exportar (simulação)
    st.download_button("Baixar Orçamento (CSV)", df_final.to_csv(), "orcamento.csv", "text/csv")
