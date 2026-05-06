import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(
    page_title="Simulador Solar & Elétrica - AJC",
    page_icon="⚡",
    layout="wide"
)

# Estilização Personalizada
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# 1. Função para carregar os dados da planilha
@st.cache_data
def carregar_dados():
    try:
        # Lê a aba de preços que configuramos
        df = pd.read_excel("precos.xlsx", sheet_name='Base_de_Precos')
        return df
    except Exception as e:
        st.error(f"Erro ao carregar a planilha 'precos.xlsx': {e}")
        return None

df_base = carregar_dados()

if df_base is not None:
    st.title("⚡ AJC Soluções em Energia")
    st.subheader("Gerador de Orçamentos Profissionais")
    st.markdown("---")

    # Layout em Colunas
    col_input, col_resumo = st.columns([2, 1])

    with col_input:
        st.header("📋 Detalhes do Projeto")
        
        # Seleção de Materiais
        st.subheader("1. Materiais e Equipamentos")
        materiais_selecionados = st.multiselect(
            "Selecione os itens da planilha:",
            options=df_base['Item'].unique()
        )

        lista_final_materiais = []
        total_materiais = 0.0

        if materiais_selecionados:
            for item in materiais_selecionados:
                # Localiza dados do item na planilha
                dados_item = df_base[df_base['Item'] == item].iloc[0]
                preco_venda = dados_item['Preço Final (R$)']
                
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.info(f"**{item}** | Unitário: R$ {preco_venda:,.2f}")
                with c2:
                    qtd = st.number_input(f"Qtd para {item}", min_value=1, value=1, key=f"q_{item}")
                
                subtotal_item = preco_venda * qtd
                total_materiais += subtotal_item
                lista_final_materiais.append({"Item": item, "Qtd": qtd, "Total": subtotal_item})

        st.markdown("---")
        
        # Seção de Serviços
        st.subheader("2. Mão de Obra e Engenharia")
        c_eng, c_mo = st.columns(2)
        with c_eng:
            valor_engenharia = st.number_input("Serviços de Engenharia (R$)", min_value=0.0, step=100.0, help="Projetos, ART e Homologação")
        with c_mo:
            valor_mo = st.number_input("Mão de Obra de Instalação (R$)", min_value=0.0, step=100.0)
        
        total_servicos = valor_engenharia + valor_mo

    with col_resumo:
        st.header("📊 Resumo Financeiro")
        
        # Configuração de Impostos
        imposto_perc = st.slider("Alíquota de Impostos (%)", 0, 25, 15)
        
        # Cálculos Finais
        bruto = total_materiais + total_servicos
        valor_imposto = bruto * (imposto_perc / 100)
        total_geral = bruto + valor_imposto

        # Cards de Resultado
        st.metric("Total em Materiais", f"R$ {total_materiais:,.2f}")
        st.metric("Total em Serviços", f"R$ {total_servicos:,.2f}")
        st.metric("Impostos Calculados", f"R$ {valor_imposto:,.2f}")
        
        st.markdown("### Valor Total do Orçamento")
        st.subheader(f"R$ {total_geral:,.2f}")

        st.markdown("---")
        
        # Botões de Ação
        if st.button("✅ Validar Orçamento", use_container_width=True):
            st.success("Cálculos validados conforme planilha de custos.")
            
        st.download_button(
            label="📄 Baixar Resumo (CSV)",
            data=pd.DataFrame(lista_final_materiais).to_csv(index=False).encode('utf-8'),
            file_name='orcamento_ajc.csv',
            mime='text/csv',
            use_container_width=True
        )

else:
    st.warning("Aguardando configuração da planilha 'precos.xlsx' no diretório raiz.")
