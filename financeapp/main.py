import streamlit as st
from datetime import date
import sqlite3
import pandas as pd


# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('finances.db')
    return conn

# Função para obter saldo atual
def get_current_balance():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT SUM(amount) FROM transactions")
    result = c.fetchone()[0]
    conn.close()
    return result if result else 0.0

# Função para obter histórico
def get_historic():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT date, description, amount FROM transactions")
    historic = c.fetchall()
    conn.close()
    return historic

# Função para adicionar transação
def add_transaction(description, amount):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO transactions (date, description, amount) VALUES (?, ?, ?)", 
              (date.today().strftime("%d/%m/%Y"), description, amount))
    conn.commit()
    conn.close()

# Função para limpar o banco de dados
def clear_database():
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()
    c.execute("DELETE FROM transactions")  # Remove todos os dados da tabela
    conn.commit()  # Confirma a transação
    conn.close()
    print("Todos os dados foram removidos da tabela 'transactions'.")


# Obtendo saldo atual
saldo_atual = get_current_balance()

# Título
st.title("Dashboard de Finanças")

# Saldo Inicial
col1_saldo, col2_caixinha = st.columns(2)
with col1_saldo:
    if "initial_balance_set" not in st.session_state:
        st.session_state.initial_balance_set = False

    if not st.session_state.initial_balance_set:
        st.subheader("Definir Saldo Inicial")
        saldo = st.number_input("Insira seu saldo inicial", min_value=0.0, step=0.01, format="%.2f")
        if st.button("Salvar Saldo Inicial"):
            add_transaction("Saldo Inicial", saldo)
            st.session_state.initial_balance_set = True
            st.experimental_set_query_params(rerun='1')

    # Mostrar saldo atual
    st.subheader(f"Seu saldo atual: R$ {saldo_atual:.2f}")

with col2_caixinha:
    st.subheader("Caixinha")

# Entrada e Saída
st.divider()
col1_input, col2_output = st.columns(2)

with col1_input:
    st.header("Entradas")
    input_value = st.number_input("R$ de entrada:", min_value=0.0, placeholder="R$")
    input_comment = st.text_input("Comentário sobre a entrada")
    if st.button("Registrar Entrada"):
        if input_value > 0:
            add_transaction(input_comment, input_value)
            st.experimental_set_query_params(rerun='1')
            st.success('Entrada inserida!', icon="✅")
with col2_output:
    st.header("Saídas")
    output_value = st.number_input("R$ de saída:", min_value=0.0, placeholder="R$")
    output_comment = st.text_input("Comentário sobre a saída")
    if st.button("Registrar Saída"):
        if output_value > 0:
            add_transaction(output_comment, -output_value)
            st.experimental_set_query_params(rerun='1')
            st.success('Saída registrada!', icon="✅")

# Histórico
st.divider()
col1_historic, col2_delete = st.columns(2)
on = st.toggle("Ver histórico")

with col1_historic:
    if on:
        st.session_state['on'] = True
        st.write("HISTÓRICO")
        historic = get_historic()
        df = pd.DataFrame(historic, columns=["Data", "Descrição", "Valor"])
        st.table(df.style.format({"Valor": "{:.2f}"}))

with col2_delete:
    if st.button("Limpar Histórico"):
        clear_database()
