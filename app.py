import streamlit as st
import pandas as pd
from pipeline_02 import pipeline
import psycopg2

# Título do dashboard
st.title('Processador de Arquivos')

# Função para processar os logs
def processar_logs():
    logs = pipeline()
    return pd.DataFrame(logs, columns=['Log'])  # Transforma os logs em DataFrame

# Botão para iniciar o processamento
if st.button('Processar'):
    with st.spinner('Processando...'):
        logs_df = processar_logs()
        st.success('Processamento concluído com sucesso!')

# Exibe o DataFrame dos logs no dashboard
st.subheader('Logs Processados')
if 'logs_df' in locals():
    st.write(logs_df)

# Função para conectar ao banco de dados PostgreSQL
def conectar_banco():
    conn = psycopg2.connect(
        host="dpg-cnp586ljm4es738i5vmg-a.oregon-postgres.render.com",
        database="dbname_uvgn",
        user="dbuser",
        password="ylxCRog1LaQ6upKtA17j5EFHElh0YJGu"
    )
    return conn

# Função para executar consultas SQL no banco de dados e retornar um DataFrame
def executar_consulta(query, conn):
    df = pd.read_sql(query, conn)
    return df

# Função para plotar um gráfico com base nos dados
def plotar_grafico(df):
    st.line_chart(df)

# Título do dashboard
st.title('Dashboard do Banco de Dados PostgreSQL')

# Conexão com o banco de dados
conn = conectar_banco()

# Query SQL para recuperar os dados do banco de dados
query = "SELECT total_vendas, valor, categoria FROM vendas_calculado"  # Substitua sua_tabela pelo nome da sua tabela

# Executa a consulta SQL e obtém os dados em um DataFrame
df = executar_consulta(query, conn)

# Query SQL para recuperar os dados do banco de dados
query = "SELECT categoria, SUM(total_vendas) AS total_vendas, SUM(valor) AS total_valor FROM vendas_calculado GROUP BY categoria"  

# Executa a consulta SQL e obtém os dados em um DataFrame
df = executar_consulta(query, conn)

# Verifica se há dados para exibir
if not df.empty:
    # Exibe os dados
    st.subheader('Dados do Banco de Dados')
    st.write(df)

    # Plotar gráfico
    st.subheader('Gráfico de Barras Agrupadas')
    st.bar_chart(df.set_index('categoria'))  # Define a coluna 'categoria' como índice para agrupar barras
else:
    st.write('Não há dados para exibir.')