import pandas as pd  # Importa a biblioteca Pandas para manipulação de dados
import streamlit as st  # Importa a biblioteca Streamlit para criar a interface
import seaborn as sns  # Importa a biblioteca Seaborn para visualização de dados
import matplotlib.pyplot as plt  # Importa a biblioteca Matplotlib para gráficos

# Carrega o arquivo CSV "Amazon-Products.csv" para um DataFrame df
df = pd.read_csv("Amazon-Products.csv", delimiter=";", encoding="UTF-8")

# Define a exibição de todas as colunas do DataFrame
pd.set_option("display.max_columns", None)
# Define a exibição de todas as linhas do DataFrame
pd.set_option("display.max_rows", None)

# Converte a coluna 'no_of_ratings' para tipo numérico, ignorando erros e substituindo valores inválidos por NaN
df['no_of_ratings'] = pd.to_numeric(df['no_of_ratings'], errors='coerce')
# Remove as linhas do DataFrame onde a coluna 'no_of_ratings' possui valores NaN
df = df.dropna(subset=['no_of_ratings'])

# Converte a coluna 'ratings' para tipo numérico, ignorando erros e substituindo valores inválidos por NaN
df['ratings'] = pd.to_numeric(df['ratings'], errors='coerce')
# Remove as linhas do DataFrame onde a coluna 'ratings' possui valores NaN
df = df.dropna(subset=['ratings'])

# Remove vírgulas da coluna 'actual_price' e 'discount_price' e converte para tipo float
df['actual_price'] = df['actual_price'].str.replace(',', '').astype(float)
df['discount_price'] = df['discount_price'].str.replace(',', '').astype(float)

# Calcula a renda com desconto e sem desconto multiplicando 'discount_price' e 'actual_price' pela quantidade de avaliações
df['renda_com_desconto'] = df['discount_price'] * df['no_of_ratings']
df['renda_sem_desconto'] = df['actual_price'] * df['no_of_ratings']

# Agrupa o DataFrame por 'main_category' e retorna o índice do produto com o maior número de avaliações em cada categoria
max_por_categoria = df.groupby('main_category')['no_of_ratings'].idxmax()
# Seleciona os produtos com o maior número de avaliações em cada categoria e reseta o índice
first_max_por_categoria = df.loc[max_por_categoria].reset_index()
# Seleciona as colunas relevantes para análise
resultado_categorias = first_max_por_categoria[['name', 'main_category', 'sub_category', 'no_of_ratings', 'ratings', 'discount_price', 'actual_price', 'renda_com_desconto', 'renda_sem_desconto', 'link']]

# Imprime no console os produtos com maior número de avaliações em cada categoria em ordem alfabética
print("Produtos com maior número de avaliações agrupados em cada categoria em ordem alfabética: ")
print(resultado_categorias.to_string())

# Exibe os produtos com maior número de avaliações em cada categoria em ordem alfabética na interface do Streamlit
st.write("Produtos com maior número de avaliações agrupados em cada categoria em ordem alfabética: ")
st.dataframe(resultado_categorias.head(10))
st.write("Obs: como não tem nenhuma coluna que indique o número de vendas com o preço com desconto ou sem"
         "desconto, usei o número de avaliações como um número mínimo de vendas de cada produto. Multipliquei"
         "o valor de cada produto com desconto e sem desconto com o número de avaliações para ter mais"
         "ou menos uma noção de lucro se todas as pessoas tivessem comprado com desconto ou sem desconto. "
         "Criei as colunas renda_com_desconto e renda_sem_desconto para representar esses dados.")

# Cria um gráfico de barras utilizando Seaborn para visualizar os produtos com maior número de avaliações em cada categoria
st.write("Produtos com maior número de avaliações em cada categoria de maneira decrescente: ")
st.set_option('deprecation.showPyplotGlobalUse', False) #Removendo qualquer mensagem de aviso do Streamlit de funções deprecated
resultado_ordenado_categorias = resultado_categorias.sort_values(by='no_of_ratings', ascending=False).reset_index(drop=True)
sns.barplot(data=resultado_ordenado_categorias.head(10), x='main_category', y='no_of_ratings')
plt.xticks(rotation=80)  # Rotaciona os rótulos do eixo x para facilitar a leitura
st.pyplot()  # Exibe o gráfico na interface do Streamlit


# max_por_subcategoria = df.groupby('sub_category')['no_of_ratings'].idxmax()
# first_max_por_subcategoria = df.loc[max_por_subcategoria].reset_index()
# resultado_subcategorias = first_max_por_subcategoria[['name', 'main_category', 'sub_category', 'no_of_ratings', 'ratings', 'discount_price', 'actual_price', 'renda_com_desconto', 'renda_sem_desconto', 'link']]
# print("Produtos com maior número de avaliações em cada subcategoria em ordem alfabética: ")
# print(resultado_subcategorias.to_string())
#
#
# resultado_ordenado_subcategorias = resultado_subcategorias.sort_values(by='no_of_ratings', ascending=False).reset_index(drop=True)
# print("\n\nProdutos com maior número de avaliações em cada subcategoria de maneira crescente: ")
# print(resultado_ordenado_subcategorias.to_string())
#
#
# resultado_ordenado_categorias = resultado_categorias.sort_values(by='no_of_ratings', ascending=False).reset_index(drop=True)
# print("\n\nProdutos com maior número de avaliações em cada categoria de maneira crescente: ")
# print(resultado_ordenado_categorias.to_string())


# soma_actual_price = df['actual_price'].sum()
# print(f"Soma de todos os valores sem desconto: {soma_actual_price}")
#
# soma_discount_price = df['discount_price'].sum()
# print(f"Soma de todos os valores com desconto: {soma_discount_price}")
