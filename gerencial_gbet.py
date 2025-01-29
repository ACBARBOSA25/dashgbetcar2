import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")

st.image("GBET CAR LOGO.png", use_column_width=True)

df = pd.read_excel('dados.xlsx') 
fin = pd.read_excel('financeiro.xlsx')
    #df = df.sort_values("Cooperativa")

st.title("PAINEL -  GBET CAR - ADESÕES - MÊS JANEIRO 2025")

col1, col2 , col3, col4 = st.columns(4)
col5, col6, col7, col8 = st.columns(4)

adesoes = df['Situacao'].count()
with col1:
     st.metric('Quant. de Adesões', round(adesoes))

novos = df['Classificacao'].isin(['NOVO']) .sum()
with col2:
     st.metric('Adesoes Novas', round(novos))

renovacoes = df['Classificacao'].isin(['RENOVAÇÃO']) .sum()
with col3:
     st.metric('Renovacoes', round(renovacoes))

parcela = df['Parcela'].sum()
with col4:
     st.metric('Soma das Parcelas', round(parcela, 2))

media = df['Parcela'].mean()
with col5:
     st.metric('Ticket Médio', round(media, 2))

auto = df.loc[df['Tipo'] =="AUTOMOVEL"]['Parcela'].mean()
with col6:
     st.metric('Ticket Auto', round(auto,2 ))

moto = df.loc[df['Tipo'] =="MOTOCICLETA"]['Parcela'].mean()
with col7:
     st.metric('Ticket Moto', round(moto, 2))

recebido = fin['Recebido'].sum()
with col8:
     st.metric('Recebido Mês', round(recebido, 2))

st.divider()

st.write("Situação Geral das Adesões dos Escritórios")
st.bar_chart(df, x="Cooperativa", y="Situacao", color="Situacao", stack="center")

st.divider()

fig_Cooperativa = px.bar(df, x= "Cooperativa", y= "Situacao",color="Situacao",barmode="group", title= "Cooperativas")
st.plotly_chart(fig_Cooperativa, use_container_width=True)

st.divider()

tipo = df.groupby(df["Tipo"])["Placa"].count().reset_index()
fig_tipo = px.bar(tipo, x= "Tipo", y= "Placa", barmode="group",text_auto=True, color= "Tipo", title= "Quantidade por Tipo de Veículo")
st.plotly_chart(fig_tipo, use_container_width=True) 

st.divider()

result = df.groupby(df["Classificacao"])["Placa"].count().reset_index()
Classificacao = px.bar(result, x= "Classificacao", y= "Placa", barmode="group", text_auto=True, color= "Classificacao", title= "Classificacao das Adesoes")
st.plotly_chart(Classificacao, use_container_width=True) 

st.divider()

Contrato = df.groupby(df["Contrato"])["Placa"].count().reset_index()
data  = px.bar(Contrato, x= "Contrato", y= "Placa",text_auto=True, barmode="group", title= "Adesões por Datas")
st.plotly_chart(data, use_container_width=True)

st.divider()

cidade = df.groupby(df["Cidade"])[["Tipo"]].value_counts().reset_index()
fig_cidade = px.bar(cidade, x= "Cidade", y= "Tipo", text_auto=True, barmode="group", color= "Tipo", title= "Tipos de Veículo  por Cidades")
st.plotly_chart(fig_cidade, use_container_width=True) 

st.divider()

Planos = df.groupby(df["Tipo"])[["Produtos"]].value_counts().reset_index()
fig_Planos = px.bar(Planos, x= "Tipo", y= "Produtos", text_auto=True, barmode="group", color= "Produtos", title= "Planos das Adesões")
st.plotly_chart(fig_Planos, use_container_width=True) 

st.divider()

parcela = df.groupby(df["Cooperativa"])[["Parcela"]].sum().reset_index()
fig_parcela = px.bar(parcela, x= "Cooperativa", y= "Parcela",text_auto=True,  title= " R$ - Parcelas por Cooperativa")
st.plotly_chart(fig_parcela, use_container_width=True) 


parcela = df.groupby(df["Cooperativa"])[["Parcela"]].sum().reset_index()
fig = px.pie(parcela, values='Parcela', names='Cooperativa', title='Representatividade Por Cooperativas')
fig.update_layout(legend_title="Cooperativa", legend_y=0.9)
fig.update_traces(textinfo='percent+label', textposition='inside')
st.plotly_chart(fig, use_container_width=True)

st.divider()

consultor = df.groupby(df["Voluntario"])[["Classificacao"]].value_counts().reset_index()       
fig_consultor = px.bar(consultor, x= "Voluntario", y= "Classificacao",barmode="group", text_auto=True, color="Classificacao",title= " Classificacao por Consultor")
st.plotly_chart(fig_consultor, use_container_width=True) 

st.divider()

df_filtrado = df[df["Classificacao"]=="NOVO"] 
novo = df_filtrado.groupby(["Voluntario", "Tipo"]).count().reset_index()          
fig_novo = px.bar(novo, x= "Voluntario", y= "Classificacao", barmode="group",color="Tipo",text_auto=True, title= " Adesões NOVAS Por Consultor")
st.plotly_chart(fig_novo)

st.divider()

treemap = df[["Cidade", "Placa"]].groupby(by=["Cidade"])["Placa"].count().reset_index()

fig2 = px.treemap(treemap, path=["Cidade","Placa"], values = "Placa", hover_data=["Cidade"],
                  color="Cidade", title="Cidades e Placas", height=700, width=600)
fig2.update_traces(textinfo="value")
st.plotly_chart(fig2)

st.divider()

st.markdown(''':blue[PAINEL DE RECEBIMENTOS MENSAL]''')

#situacao = fin.groupby(fin["Tipo_Boleto"])["Recebido"].sum().reset_index()
#fig_tipo = px.bar(situacao, x= "Tipo_Boleto", y= "Recebido", barmode="group",text_auto=True, title= "Recebido por Tipo de Boleto")
#st.plotly_chart(fig_tipo, use_container_width=True) 
#st.divider()

boleto = fin.groupby(fin["Tipo_Boleto"])["Recebido"].sum().reset_index()
fig_tipo = px.bar(boleto, x= "Tipo_Boleto", y= "Recebido", barmode="group",text_auto=True, title= "Recebido por Tipo de Boleto")
st.plotly_chart(fig_tipo, use_container_width=True) 
st.divider()

data = fin.groupby(fin["Data_Recebido"])["Recebido"].sum().reset_index()
fig_tipo = px.bar(data, x= "Data_Recebido", y= "Recebido", barmode="group",text_auto=True, title= "Datas e Recebimentos")
st.plotly_chart(fig_tipo, use_container_width=True) 
st.divider()

treemap = fin[["Cooperativa", "Recebido"]].groupby(by=["Cooperativa"])["Recebido"].sum().reset_index()
fig2 = px.treemap(treemap, path=["Cooperativa","Recebido"], values = "Recebido", hover_data=["Cooperativa"],
                  color="Cooperativa", title="Escritórios e Recebimentos", height=700, width=600)
fig2.update_traces(textinfo="value")
st.plotly_chart(fig2)
st.divider()

voluntario = fin.groupby(fin["Voluntario"])["Recebido"].sum().reset_index()
fig_tipo = px.bar(voluntario, x= "Voluntario", y= "Recebido", barmode="group",text_auto=True, title= "Recebido por Voluntário")
st.plotly_chart(fig_tipo, use_container_width=True) 
st.divider()

baixa = fin.groupby(fin["Tipo_Baixa"])[["Usuario"]].count().reset_index()
fig = px.pie(baixa, values='Usuario', names='Tipo_Baixa', title='Tipo da Baixa dos Boletos')
fig.update_layout(legend_title="Tipo_Baixa", legend_y=0.9)
fig.update_traces(textinfo='percent+label', textposition='inside')
st.plotly_chart(fig, use_container_width=True)






