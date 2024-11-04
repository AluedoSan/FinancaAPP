import streamlit as st
import pandas as pd
import numpy as np
from datetime import date


#Onde ficará a aplicação
@st.cache_data
class Main:

    #Declaração do dicionário
    financa = {
        "saldo": float,
        "data": date.today().strftime("%d/%m/%Y"),
        "salario": float
    }
    #Título
    st.title("Dashboard")
    col1_saldo, col2_divider , col3_data = st.columns(3)
    with col1_saldo:
        st.header("Saldo")
        #Definição do saldo
        with st.popover("Inserir saldo"):
            financa["saldo"] = st.number_input(
            "Insira seu saldo", value=0, min_value=0, placeholder="R$")

        st.subheader(f"Seu saldo atual: R${financa["saldo"]}")
        


    with col2_divider:
        st.header("")

    with col3_data:
        st.header("Data")
        st.subheader(financa["data"])
        on = st.toggle("Info")
        if on:
            st.subheader("Saldo")
            st.info("É onde fica o dinheiro total da sua conta", icon="ℹ️")
            st.subheader("Entrada")
            st.info("É para caso você recebeu algo durante o mês", icon="ℹ️")
            st.subheader("Saída")
            st.info("É para quando você gastou algo")
            st.subheader("Comentário")
            st.info("É para escrever no que você gastou, ou como recebeu algo!", icon="ℹ️")

    st.divider()

    #Separar por colunas entrada/saída
    col1_entrada, col2_saida = st.columns(2)
    with col1_entrada:
        st.header("Entradas")
        input_value = st.number_input("R$ de entrada:", min_value=0,  value=None, placeholder="R$")
        st.write("The current number is ", input_value)
        if input_value != None: 
            financa["saldo"] = financa["saldo"] + input_value
        input_comment = st.text_input("Comentário sobre a entrada")

    with col2_saida:
        st.header("Saídas")
        output_value = st.number_input("R$ de saída:", min_value=0, value=None, placeholder="R$")
        st.write("The current number is ", output_value)
        output_comment = st.text_input("Comentário sobre a saída")

def entrada(saldo):
    pass
