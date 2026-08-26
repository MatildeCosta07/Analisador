import streamlit as st
import pandas as pd
import py3Dmol
from stmol import showmol
from Bio.Seq import Seq
from Bio import Restriction

# --- Configuração da Página ---
st.set_page_config(page_title="BioinfoApp", page_icon="🧬")
st.title("Análise de Sequências de DNA")

# --- Entrada de Dados ---
sequencia = st.text_area("Escreva a sequência de DNA:", value="ATGCGTA")
botao = st.button("Analisar")

# --- Lógica de Processamento ---
if botao == True and sequencia != "":
    sequencia = sequencia.upper()
    
    # ==========================================
    # O CÉREBRO: Fazer as contas todas primeiro
    # ==========================================
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
                
        st.success("Análise concluída com sucesso!")
        
        # ==========================================
        # A MONTRA: Criar os separadores e arrumar a casa
        # ==========================================
        aba_dna, aba_proteina, aba_3d, aba_enzimas = st.tabs(["🧬 Análise de DNA", "🥩 Análise de Proteína", "🌀 Estrutura 3D", "✂️ Análise de Enzimas de Restrição (Biopython)"])
        
        # --- SEPARADOR 1: DNA ---
        with aba_dna:
            st.header("Análise de DNA")
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

            st.write("### Distribuição das Bases")
            dados_grafico_dna = {"A": contagem_A, "T": contagem_T, "C": contagem_C, "G": contagem_G}
            st.bar_chart(dados_grafico_dna)

        # --- SEPARADOR 2: PROTEÍNA ---
        with aba_proteina:
            st.header("Análise da Proteína")
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

        # --- SEPARADOR 3: 3D ---
        with aba_3d:
            st.header("Estrutura 3D da Proteína")
            # Peça 1: Input e botão no caso de o utilizador não carregar no Enter
            codigo_pdb = st.text_input("Escreva o código PDB da proteína (ex: 1A2C):", value="1A2C")
            
            if codigo_pdb != "":
                try:
                    # Peça 2: Preparar o modelo
                    visualizador = py3Dmol.view(query=f"pdb:{codigo_pdb.lower()}")
                    visualizador.setStyle({'cartoon': {'color': 'spectrum'}})
                    visualizador.setBackgroundColor('#0e1117')
                    
                    # Peça 3: Mostrar
                    showmol(visualizador, height=500, width=800)
                    st.caption("Interaja com a proteína: Use o rato para rodar e faça Zoom!")
                except:
                    st.error("Não foi possível carregar esta estrutura. Verifique se o código está correto.")
        with aba_enzimas:
            st.header("Enzimas de restrição")
            sequencia_bio = Seq(sequencia)
            analise = Restriction.Analysis(Restriction.AllEnzymes, sequencia_bio)
            resultados_enzimas = analise.full()
            enzimas_encontradas = 0
            for enzima, cortes in resultados_enzimas.items():
                if len(cortes) > 0:
                    enzimas_encontradas += 1
                                
                    posicoes = ", ".join(map(str, cortes))
                                
                    st.success(f"A enzima **{enzima}** corta nas posições: **{posicoes}**")
            if enzimas_encontradas == 0:
                    st.warning("Nenhuma enzima da base de dados corta esta sequência.")
