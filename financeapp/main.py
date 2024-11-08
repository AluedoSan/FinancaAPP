import streamlit as st
from datetime import date
import sqlite3
import pandas as pd

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('finances.db')
    con = conn.execute("""CREATE TABLE IF NO EXISTS transactions(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    description TEXT,
                    amount REAL 
                       )""")
    con.commit()
    con.execute = ("""CREATE TABLE IF NOT EXISTS reserve (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_reserve TEXT NOT NULL,
                description TEXT,
                amount_reserve REAL 
                )""")
    con.commit()
    return conn

# Função para obter saldo atual
def get_current_balance():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT SUM(amount) FROM transactions")
    result = c.fetchone()[0]
    conn.close()
    return result if result else 0.0

# Função para obter o saldo da caxinha
def get_current_balance_reserve():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT SUM(amount_reserve) FROM reserve")
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

# Função para adicionar transação para a caixinha
def add_transaction_reserve(description, amount):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO reserve (date_reserve, description, amount_reserve) VALUES (?, ?, ?)", 
              (date.today().strftime("%d/%m/%Y"), description, amount))
    conn.commit()
    conn.close()

# Função para obter a última transação
def get_last_transaction():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT amount FROM transactions ORDER BY id DESC LIMIT 1")
    last_transaction = c.fetchone()
    conn.close()
    return last_transaction[0] if last_transaction else 0.0

def get_last_transaction_reserve():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT amount_reserve FROM reserve ORDER BY id DESC LIMIT 1")
    last_transaction_reserve = c.fetchone()
    conn.close()
    return last_transaction_reserve[0] if last_transaction_reserve else 0.0

# Função para limpar o banco de dados
def clear_database():
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()
    c.execute("DELETE FROM transactions")  # Remove todos os dados da tabela
    conn.commit()  # Confirma a transação
    conn.close()
    print("Todos os dados foram removidos da tabela 'transactions'.")

# Função para limpar o banco de dados
def clear_database_reserve():
    conn = sqlite3.connect('finances.db')
    c = conn.cursor()
    c.execute("DELETE FROM reserve")  # Remove todos os dados da tabela
    conn.commit()  # Confirma a transação
    conn.close()
    print("Todos os dados foram removidos da tabela 'transactions'.")

# Função para atualizar o saldo atual após inserção de transação
def update_current_balance():
    st.session_state.saldo_atual = get_current_balance()
    st.session_state.saldo_reserve = get_current_balance_reserve()

# Função para converter o dataFrame em arquivo excel
def convert_df(df):
    return df.to_csv().encode("utf-8")

# Obtendo saldo atual
ultima_transacao = get_last_transaction()
ultima_transacao_reserva = get_last_transaction_reserve()
saldo_atual,saldo_reserve = get_current_balance(), get_current_balance_reserve() 
total = saldo_atual + saldo_reserve
# Título
st.title("Dashboard de Finanças")

col1, col2, col3 = st.columns(3)
# Porcentagem de entrada e saída
# Evitar divisão por zero
if saldo_atual != 0:
    porcentagem_transacao = (ultima_transacao / saldo_atual) * 100
else:
    porcentagem_transacao = 0
# Porcentagem da reserva
if saldo_reserve != 0:
    porcentagem_transacao_reserva = (ultima_transacao_reserva / saldo_reserve) * 100
else:
    porcentagem_transacao_reserva = 0
col1.metric("Total", f"{total:.2f}", f"{porcentagem_transacao:.2f}%")
col2.metric("Saldo", f"{saldo_atual:.2f}", f"{porcentagem_transacao:.2f}%")
col3.metric("Reserva", f"{saldo_reserve:.2f}", f"{porcentagem_transacao_reserva:.2f}%")

# Saldo Inicial
col1_saldo, col2_caixinha = st.columns(2)
with col1_saldo:
    if "initial_balance_set" not in st.session_state:
        st.session_state.initial_balance_set = False

    if not st.session_state.initial_balance_set:
        st.subheader("Definir Saldo Inicial")
        saldo = st.number_input("Insira seu saldo inicial:", min_value=0.0, step=0.01, format="%.2f")
        if st.button("Salvar Saldo Inicial"):
            add_transaction("Saldo Inicial", saldo)
            st.session_state.initial_balance_set = True
            st.experimental_set_query_params(rerun='1')


with col2_caixinha:
    st.subheader("Reserva")
    if "initial_balance_set" not in st.session_state:
        st.session_state.initial_balance_set = False

    if not st.session_state.initial_balance_set:
        saldo_caixinha = st.number_input("Saldo reserva:", step=0.01, format="%.2f")
        if st.button("Salvar"):
            add_transaction_reserve("Saldo caixinha", saldo_caixinha)
            st.session_state.initial_balance_set = True
            st.experimental_set_query_params(rerun='1')


# Entrada e Saída
st.divider()
col1_input, col2_output = st.columns(2)

with col1_input:
    st.header("Entradas")
    with st.popover("Registrar entrada"):
        input_value = st.number_input("R$ de entrada:", min_value=0.0, placeholder="R$")
        input_comment = st.text_input("Comentário sobre a entrada")
        if st.button("Registrar Entrada"):
            if input_value > 0:
                add_transaction(input_comment, input_value)
                update_current_balance()
                st.success('Entrada inserida!', icon="✅")

with col2_output:
    st.header("Saídas")
    with st.popover("Registrar saída"):
        output_value = st.number_input("R$ de saída:", min_value=0.0, placeholder="R$")
        output_comment = st.text_input("Comentário sobre a saída")
        if st.button("Registrar Saída"):
            if output_value > 0:
                add_transaction(output_comment, -output_value)
                update_current_balance()
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
    with st.popover("Limpar Histórico"):
        if st.button("Saldo"):
            clear_database()
        if st.button("Reserva"):
            clear_database_reserve()
    
    historic = get_historic()
    df = pd.DataFrame(historic)
    csv = convert_df(df)
    st.download_button(
        label="Download data",
        data=csv,
        file_name="extrato.csv",
        mime="text/csv",
    )
