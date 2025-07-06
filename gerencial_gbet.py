import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")

st.image("GBET CAR LOGO.png", use_column_width=True)

df = pd.read_excel('dados.xlsx') 
fin = pd.read_excel('financeiro.xlsx')
df = df.sort_values("Cooperativa")

filtro_Cooperativa = st.sidebar.multiselect('Filtrar Adesões por Escritórios', df["Cooperativa"].unique()) 
df_filtered = df[df["Cooperativa"].isin(filtro_Cooperativa)] if  filtro_Cooperativa else df

filtro_financeiro = st.sidebar.multiselect('Filtro Recebimentos por Escritórios', fin["Cooperativa"].unique()) 
fin_filtered = fin[fin["Cooperativa"].isin(filtro_financeiro)] if  filtro_financeiro else fin

st.title("PAINEL - ADESÕES e FINANCEIRO - JULHO 2025")

col1, col2 , col3, col4 = st.columns(4)
col5, col6, col7, col8 = st.columns(4)

adesoes = df['Situacao'].count()
with col1:
     st.metric("Quant. de Adesões", round(adesoes),border=True)

novos = df['Classificacao'].isin(['NOVO']).sum()
with col2:
     st.metric("Adesoes Novas", round(novos), border=True)

renovacoes = df['Classificacao'].isin(['RENOVAÇÃO']).sum()
with col3:
     st.metric('Renovacoes', round(renovacoes), border=True)

parcela = df['Parcela'].sum()
with col4:
     st.metric('Soma das Parcelas', round(parcela, 2), border=True)

media = df['Parcela'].mean()
with col5:
     st.metric('Ticket Médio', round(media, 2), border=True)

auto = df.loc[df['Tipo'] =="AUTOMOVEL"]['Parcela'].mean()
with col6:
     st.metric('Ticket Auto', round(auto,2 ), border=True)

moto = df.loc[df['Tipo'] =="MOTOCICLETA"]['Parcela'].mean()
with col7:
     st.metric('Ticket Moto', round(moto, 2), border=True)

recebido = fin['Recebido'].sum()
with col8:
     st.metric('Recebido Mês', round(recebido, 2),border=True )

st.divider()

 
st.write("Situação Geral das Adesões dos Escritórios")
st.bar_chart(df, x="Cooperativa", y="Situacao", color="Situacao", stack="center")

st.divider()


cooperativa = px.bar(df_filtered, x= "Cooperativa", y= "Situacao",color="Situacao",barmode="group", title= "Cooperativas")
st.plotly_chart(cooperativa, use_container_width=True)

st.divider()

 
ticket = df_filtered.groupby(["Cooperativa", "Tipo"])["Parcela"].mean().round(2).reset_index()        
fig_novo = px.bar(ticket, x= "Cooperativa", y= "Tipo", color="Tipo", barmode="group",text="Parcela", title= " TICKET MÉDIO POR ESCRITÓRIO")
st.plotly_chart(fig_novo) 

st.divider()

adesoes = df_filtered.groupby(["Cooperativa", "Classificacao"])["Nome"].count().reset_index()
classificacao = px.bar(adesoes, x= "Cooperativa", y= "Classificacao",barmode="group",text="Nome",color="Classificacao", title= "Adesões por Cooperativas")
st.plotly_chart(classificacao, use_container_width=True) 

st.divider()

tipo = df_filtered.groupby(["Tipo"])["Placa"].count().reset_index()
fig_tipo = px.bar(tipo, x= "Tipo", y= "Placa", barmode="group",text_auto=True, color= "Tipo", title= "Quantidade por Tipo de Veículo")
st.plotly_chart(fig_tipo, use_container_width=True) 

st.divider()

classific = df_filtered.groupby(df["Classificacao"])["Placa"].count().reset_index()
Classificacao = px.bar(classific, x= "Classificacao", y= "Placa", barmode="group", text_auto=True, color= "Classificacao", title= "Classificacao das Adesoes")
st.plotly_chart(Classificacao, use_container_width=True) 

st.divider()

datas = df_filtered.groupby(df["Contrato"])["Placa"].count().reset_index()
data  = px.bar(datas, x= "Contrato", y= "Placa",text_auto=True, barmode="group", title= "Adesões por Datas")
st.plotly_chart(data, use_container_width=True)

st.divider()

tipo = df_filtered.groupby(["Cidade","Tipo"])["Nome"].count().reset_index()
fig_cidade = px.bar(tipo, x= "Cidade", y= "Tipo", text="Nome", barmode="group", color= "Tipo", title= "Tipos de Veículo  por Cidades")
st.plotly_chart(fig_cidade, use_container_width=True) 

st.divider()

planos = df_filtered.groupby(["Tipo","Produtos"])["Nome"].count().reset_index()
fig_Planos = px.bar(planos, x= "Tipo", y= "Produtos", text="Nome", barmode="group", color= "Produtos", title= "Planos das Adesões")
st.plotly_chart(fig_Planos, use_container_width=True) 

st.divider()

parcelas = df_filtered.groupby(df["Cooperativa"])[["Parcela"]].sum().reset_index()
fig_parcela = px.bar(parcelas, x= "Cooperativa", y= "Parcela",text_auto=True,  title= " R$ - Parcelas por Cooperativa")
st.plotly_chart(fig_parcela, use_container_width=True) 


representa = df_filtered.groupby(["Cooperativa"])[["Parcela"]].sum().reset_index()
fig = px.pie(representa, values='Parcela', names='Cooperativa', title='Representatividade Por Cooperativas')
fig.update_layout(legend_title="Cooperativa", legend_y=0.9)
fig.update_traces(textinfo='percent+label', textposition='inside')
st.plotly_chart(fig, use_container_width=True)

st.divider()

df_grouped = df_filtered.groupby(["Voluntario","Classificacao"])["Nome"].count().reset_index()       
fig_consultor = px.bar(df_grouped, x= "Voluntario", y= "Classificacao",barmode="group",color="Classificacao", text="Nome",title= " Classificacao por Consultor")
st.plotly_chart(fig_consultor, use_container_width=True) 

st.divider()

novos = df[df["Classificacao"]=="NOVO"] 
novo = df_filtered.groupby(["Voluntario", "Tipo"]).count().reset_index()          
fig_novo = px.bar(novo, x= "Voluntario", y= "Classificacao", color="Tipo", barmode="group",text_auto=True, title= " Adesões NOVAS Por Consultor")
st.plotly_chart(fig_novo) 

st.divider()

treemap = df_filtered[["Cidade", "Placa"]].groupby(by=["Cidade"])["Placa"].count().reset_index()

fig2 = px.treemap(treemap, path=["Cidade","Placa"], values = "Placa", hover_data=["Cidade"],
                  color="Cidade", title="Cidades e Placas", height=700, width=600)
fig2.update_traces(textinfo="value")
st.plotly_chart(fig2)

st.divider()

st.markdown(''':blue[PAINEL DE RECEBIMENTOS MENSAL]''')


boleto = fin_filtered.groupby(["Tipo_Boleto"])["Recebido"].sum().reset_index()
fig_tipo = px.bar(boleto, x= "Tipo_Boleto", y= "Recebido", barmode="group",text_auto=True, title= "Recebido por Tipo de Boleto")
st.plotly_chart(fig_tipo, use_container_width=True) 
st.divider()

data = fin_filtered.groupby(["Data_Recebido"])["Recebido"].sum().reset_index()
fig_tipo = px.bar(data, x= "Data_Recebido", y= "Recebido", barmode="group",text_auto=True, title= "Datas e Recebimentos")
st.plotly_chart(fig_tipo, use_container_width=True) 
st.divider()

treemap = fin_filtered[["Cooperativa", "Recebido"]].groupby(by=["Cooperativa"])["Recebido"].sum().reset_index()
fig2 = px.treemap(treemap, path=["Cooperativa","Recebido"], values = "Recebido", hover_data=["Cooperativa"],
                  color="Cooperativa", title="Escritórios e Recebimentos", height=700, width=600)
fig2.update_traces(textinfo="value")
st.plotly_chart(fig2)
st.divider()

voluntario = fin_filtered.groupby(["Voluntario"])["Recebido"].sum().reset_index()
fig_tipo = px.bar(voluntario, x= "Voluntario", y= "Recebido", barmode="group",text_auto=True, title= "Recebido por Voluntário")
st.plotly_chart(fig_tipo, use_container_width=True) 
st.divider()

baixa = fin_filtered.groupby(["Tipo_Baixa"])[["Usuario"]].count().reset_index()
fig = px.pie(baixa, values='Usuario', names='Tipo_Baixa', title='Tipo da Baixa dos Boletos')
fig.update_layout(legend_title="Tipo_Baixa", legend_y=0.9)
fig.update_traces(textinfo='percent+label', textposition='inside')
st.plotly_chart(fig, use_container_width=True)



