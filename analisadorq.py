import streamlit as st
import pandas as pd

st.set_page_config(page_title="BioinfoApp", page_icon="🧬")
st.title("Análise de Sequências de DNA")

sequencia = st.text_area("Escreva a sequência de DNA:", value="ATGCGTA")
botao = st.button("Analisar")

if botao == True and sequencia != "":
    sequencia = sequencia.upper()
    
    contagem = len(sequencia)
    contagem_A = sequencia.count("A")
    contagem_T = sequencia.count("T")
    contagem_C = sequencia.count("C")
    contagem_G = sequencia.count("G")

    soma_bases = contagem_A + contagem_T + contagem_C + contagem_G

    if soma_bases != contagem:
        st.error("Erro: A sequência contém caracteres inválidos! Por favor, utilize apenas A, T, C ou G.")
    else:
        conteudo_GC = (contagem_G + contagem_C) / contagem
        
        tabela_codoes = {
            "ATA": "I", "ATC": "I", "ATT": "I", "ATG": "M",
            "ACA": "T", "ACC": "T", "ACG": "T", "ACT": "T",
            "AAC": "N", "AAT": "N", "AAA": "K", "AAG": "K",
            "AGC": "S", "AGT": "S", "AGA": "R", "AGG": "R",
            "CTA": "L", "CTC": "L", "CTG": "L", "CTT": "L",
            "CCA": "P", "CCC": "P", "CCG": "P", "CCT": "P",
            "CAC": "H", "CAT": "H", "CAA": "Q", "CAG": "Q",
            "CGA": "R", "CGC": "R", "CGG": "R", "CGT": "R",
            "GTA": "V", "GTC": "V", "GTG": "V", "GTT": "V",
            "GCA": "A", "GCC": "A", "GCG": "A", "GCT": "A",
            "GAC": "D", "GAT": "D", "GAA": "E", "GAG": "E",
            "GGA": "G", "GGC": "G", "GGG": "G", "GGT": "G",
            "TCA": "S", "TCC": "S", "TCG": "S", "TCT": "S",
            "TTC": "F", "TTT": "F", "TTA": "L", "TTG": "L",
            "TAC": "Y", "TAT": "Y", "TAA": "*", "TAG": "*",
            "TGC": "C", "TGT": "C", "TGA": "*", "TGG": "W"
        }

        pesos_moleculares = {
            "A": 89.1, "R": 174.2, "N": 132.1, "D": 133.1, "C": 121.2,
            "Q": 146.1, "E": 147.1, "G": 75.1, "H": 155.2, "I": 131.2,
            "L": 131.2, "K": 146.2, "M": 149.2, "F": 165.2, "P": 115.1,
            "S": 105.1, "T": 119.1, "W": 204.2, "Y": 181.2, "V": 117.1,
            "*": 0.0, "?": 0.0
        }

        inicio = sequencia.find("ATG")
        proteina = ""
        peso_total = 0.0
        
        if inicio != -1:
            for i in range(inicio, contagem, 3):
                codao = sequencia[i:i+3]
                if len(codao) == 3:
                    amino = tabela_codoes.get(codao, "?")
                    proteina += amino
                    peso_total += pesos_moleculares.get(amino, 0.0)
        else:
            proteina = "Nenhum codão de iniciação (ATG) encontrado."
                
        # --- Apresentação Visual ---
        st.success("Análise concluída com sucesso!")
        
        if conteudo_GC > 0.6:
            st.warning(f"Atenção: Esta sequência tem um conteúdo GC elevado! ({conteudo_GC * 100:.1f}%)")
        else:
            st.info(f"O conteúdo GC desta sequência está dentro de valores normais. ({conteudo_GC * 100:.1f}%)")
            
        st.header("1. Análise de DNA")
        
        if conteudo_GC > 0.6:
            st.warning(f"Atenção: Esta sequência tem um conteúdo GC elevado! ({conteudo_GC * 100:.1f}%)")
        else:
            st.info(f"O conteúdo GC desta sequência está dentro de valores normais. ({conteudo_GC * 100:.1f}%)")

        st.write("### Contagens Detalhadas")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric(label="Total de Bases", value=contagem)
        with col2:
            st.metric(label="Adeninas (A)", value=contagem_A)
        with col3:
            st.metric(label="Timinas (T)", value=contagem_T)
        with col4:
            st.metric(label="Citosinas (C)", value=contagem_C)
        with col5:
            st.metric(label="Guaninas (G)", value=contagem_G)

        st.write("### Distribuição das Bases de DNA")
        dados_grafico_dna = {
            "A": contagem_A, 
            "T": contagem_T, 
            "C": contagem_C, 
            "G": contagem_G 
        }
        st.bar_chart(dados_grafico_dna)

        st.header("2. Análise da Proteína")
        
        if inicio != -1:
            st.info(proteina)
            
            st.write(f"**Total de Aminoácidos:** {len(proteina)}")
            st.write(f"**Peso Molecular Estimado:** {peso_total:.2f} Da (Daltons)")
            
            analise_aa = {}
            for letra in set(proteina):
                analise_aa[letra] = proteina.count(letra)
            
            st.write("### Distribuição de Aminoácidos")
            tabela_grafico = pd.DataFrame(list(analise_aa.items()), columns=["Aminoácido", "Quantidade"])
            st.bar_chart(tabela_grafico, x="Aminoácido", y="Quantidade")
        else:
            st.warning(proteina)
