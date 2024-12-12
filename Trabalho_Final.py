import numpy as np
import sqlite3
import streamlit as st
from dataclasses import dataclass
import subprocess

# Nome do arquivo a ser executado
arquivo = "Trabalho_Final.py"

# Comando para rodar com Streamlit
comando = ["streamlit", "run", arquivo]

try:
    # Executa o comando no terminal
    subprocess.run(comando, check=True)
except FileNotFoundError:
    print("Erro: Certifique-se de que o Streamlit está instalado e no PATH.")
except subprocess.CalledProcessError as e:
    print(f"Erro ao executar o comando: {e}")

# Configuração do Streamlit
st.set_page_config(
    page_title='Calculadora de Matrizes com Banco',
    layout="wide",
    initial_sidebar_state="expanded",
)

# Conexão com o banco de dados
banco = sqlite3.connect("banco.db")
cursor = banco.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS matriz (matrizA TEXT, matrizU TEXT, matrizL TEXT)")

@dataclass
class Matriz:
    matrizI: np.ndarray

    def LU(self):
        n = len(self.matrizI)
        u = np.zeros_like(self.matrizI)
        l = np.eye(n)

        for i in range(n):
            # Calcula os elementos de U
            for j in range(i, n):
                u[i][j] = self.matrizI[i][j] - sum(l[i][k] * u[k][j] for k in range(i))
            # Calcula os elementos de L
            for j in range(i + 1, n):
                l[j][i] = (self.matrizI[j][i] - sum(l[j][k] * u[k][i] for k in range(i))) / u[i][i]

        return u, l

    def salvar_no_banco(self, u, l):
        stringA = self._matriz_para_string(self.matrizI)
        stringU = self._matriz_para_string(u)
        stringL = self._matriz_para_string(l)

        cursor.execute("INSERT INTO matriz (matrizA, matrizU, matrizL) VALUES (?, ?, ?)", (stringA, stringU, stringL))
        banco.commit()

    @staticmethod
    def _matriz_para_string(matriz):
        return ';'.join([','.join(map(str, linha)) for linha in matriz])

    @staticmethod
    def _string_para_matriz(string_matriz):
        linhas = string_matriz.split(';')
        return np.array([list(map(float, linha.split(','))) for linha in linhas])

    @staticmethod
    def buscar_por_indice(indice):
        try:
            cursor.execute("SELECT matrizA, matrizU, matrizL FROM matriz LIMIT 1 OFFSET ?", (indice,))
            resultado = cursor.fetchone()
            if resultado:
                matrizA = Matriz._string_para_matriz(resultado[0])
                matrizU = Matriz._string_para_matriz(resultado[1])
                matrizL = Matriz._string_para_matriz(resultado[2])
                return matrizA, matrizU, matrizL
            else:
                return None, None, None
        except Exception as e:
            st.error(f"Erro ao buscar a matriz: {e}")
            return None, None, None

# Função para entrada de matrizes
def entrada_matriz(nome_matriz, tamanho_matriz):
    st.write(f"Preencha os valores para {nome_matriz}:")
    matriz = []
    for i in range(tamanho_matriz):
        linha = []
        cols = st.columns(tamanho_matriz)
        for j in range(tamanho_matriz):
            valor = cols[j].number_input(f"{nome_matriz} ({i + 1},{j + 1})", min_value=None, max_value=None, key=f"{nome_matriz}_{i}_{j}", step=1.0)
            linha.append(valor)
        matriz.append(linha)
    return np.array(matriz)

def somar_matrizes(matriz1, matriz2):
    return np.add(matriz1, matriz2)

def subtrair_matrizes(matriz1, matriz2):
    return np.subtract(matriz1, matriz2)

# Função para multiplicar duas matrizes
def multiplicar_matrizes(matriz1, matriz2):
    return np.dot(matriz1, matriz2)

# Interface do Streamlit
st.title("Calculadora de Matrizes com Banco")

# Entrada para tamanho da matriz
tamanho_matriz = st.number_input("Tamanho da matriz (n x n):", min_value=1, max_value=7, step=1)

col1, col2, col3 = st.columns([4, 2, 4])

with col1:
    st.subheader("Matriz 1")
    matriz1 = entrada_matriz("Matriz 1", tamanho_matriz)
    if st.button("Calcular LU para Matriz 1"):
        try:
            m1 = Matriz(matriz1)
            u, l = m1.LU()
            m1.salvar_no_banco(u, l)
            st.write("Decomposição LU salva no banco de dados:")
            st.write("Matriz U:", u)
            st.write("Matriz L:", l)
        except Exception as e:
            st.error(f"Erro: {e}")

with col2:
    st.write("")  # Espaço vazio
    somar_btn = st.button("Somar Matrizes")
    subtrair_matrizes_btn = st.button("Subtrair Matrizes")
    multiplicar_matrizes_btn = st.button("Multiplicar Matriz 1 e Matriz 2")
    # Botão para buscar matrizes individuais
    st.subheader("Buscar uma Matriz do Banco")

    indice_matriz = st.number_input("Digite o índice da matriz que deseja buscar (começando de 0):", min_value=0,
                                    step=1)

    if st.button("Buscar Matriz Individual"):
        matrizA, matrizU, matrizL = Matriz.buscar_por_indice(indice_matriz)
        if matrizA is not None:
            st.subheader(f"Matriz {indice_matriz} - Original:")
            st.write(matrizA)
            st.subheader(f"Matriz {indice_matriz} - U:")
            st.write(matrizU)
            st.subheader(f"Matriz {indice_matriz} - L:")
            st.write(matrizL)
        else:
            st.error("Nenhuma matriz encontrada com o índice especificado.")



with col3:
    st.subheader("Matriz 2")
    matriz2 = entrada_matriz("Matriz 2", tamanho_matriz)
    if st.button("Calcular LU para Matriz 2"):
        try:
            m2 = Matriz(matriz2)
            u, l = m2.LU()
            m2.salvar_no_banco(u, l)
            st.write("Decomposição LU salva no banco de dados:")
            st.write("Matriz U:", u)
            st.write("Matriz L:", l)
        except Exception as e:
            st.error(f"Erro: {e}")

# Exibindo os resultados
if somar_btn:
    try:
        resultado = somar_matrizes(matriz1, matriz2)
        st.subheader("Resultado da Soma:")
        st.write(resultado)
    except Exception as e:
        st.error(f"Ocorreu um erro ao somar as matrizes: {e}")

if subtrair_matrizes_btn:
    try:
        resultado1 = subtrair_matrizes(matriz1, matriz2)
        st.subheader("Resultado da Subtração:")
        st.write(resultado1)
    except Exception as e:
        st.error(f"Ocorreu um erro ao subtrair a matriz: {e}")

if multiplicar_matrizes_btn:
    try:
        resultado2 = multiplicar_matrizes(matriz1, matriz2)
        st.subheader("Resultado da Multiplicação (Matriz 1 x Matriz 2):")
        st.write(resultado2)
    except ValueError as e:
        st.error(f"Erro: Não é possível multiplicar matrizes de tamanhos incompatíveis: {e}")
    except Exception as e:
        st.error(f"Ocorreu um erro ao multiplicar as matrizes: {e}")


# Fechar a conexão ao final
banco.close()
