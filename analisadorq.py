import streamlit as st
# interface #
st.set_page_config(page_title="BioinfoApp", page_icon="🧬")
st.title("Análise de Sequencias de DNA")
sequencia = st.text_area("Escreva a sequencia de DNA:", value= "ATGCGTA")
botao = st.button("Analisar")

if botao == True and sequencia != "":
    sequencia = sequencia.upper()
    contagem = len(sequencia)
    contagem_A = sequencia.count("A")
    contagem_T = sequencia.count("T")
    contagem_C = sequencia.count("C")
    contagem_G = sequencia.count("G")

    conteudo_GC = (contagem_G + contagem_C) / contagem
    st.success("Análise concluída com sucesso!")

    if conteudo_GC > 0.6:
        st.warning("Atenção: Esta sequência tem um conteúdo GC elevado!")
    else:
        st.info("O conteúdo GC desta sequência está dentro de valores normais.")

    soma_bases = contagem_A + contagem_T + contagem_C + contagem_G

    
    if soma_bases != contagem:
        st.error("Erro: A sequência contém caracteres inválidos! Por favor, utilize apenas A, T, C ou G.")

    dados_grafico = {
    "A": contagem_A, 
    "T": contagem_T, 
    "C": contagem_C, 
    "G": contagem_G }
    st.bar_chart(dados_grafico)


    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(label="Contagem do DNA", value=contagem)
    with col2:
        st.metric(label="Contagem de Adeninas", value=contagem_A)
    with col3:
        st.metric(label="Contagem de Timinas", value=contagem_T)
    with col4:
        st.metric(label="Contagem de Citosinas", value=contagem_C)
    with col5:
        st.metric(label="Contagem de Guaninas", value=contagem_G)




