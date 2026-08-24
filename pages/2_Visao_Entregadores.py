#titulo 
import io
import re
import pandas as pd
from haversine import haversine
import streamlit as st
from datetime import datetime
from PIL import Image
import plotly.express as px
import folium
from streamlit_folium import folium_static
st.set_page_config(page_title = 'Visão Entregadores', page_icon='XD', layout='wide')
df = pd.read_csv('dataset/train.csv')


df1 = df.copy()

linhas_selecionadas = (df1['Festival'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()


linhas_selecionadas = (df1['Delivery_location_latitude'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN')
df1 = df1.loc[linhas_selecionadas, :].copy()


linhas_selecionadas = (df1['City'] != 'NaN')
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['City'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()

#limpeza dos dados Coluna Age
linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()

df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

#limpeza coluna ratings
df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)


#coluna Ordeer Date
df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

#coluna multiple_deleveries
linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()
df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

#Removendo os espaços
df1 = df1.reset_index(drop=True)
for i in range(len(df1)):
  df1.loc[i, 'ID'] = df1.loc[i,'ID']

#removendo os espaços mais leve
df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
#limpando a coluna time taken 
df1['Time_taken(min)']= df1['Time_taken(min)'].apply(lambda x: x.split ('(min) ') [1] )
df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)



#Quantidade de pedidos por dia
#colunas
cols = ['ID', 'Order_Date']

#linhas
df_aux = df1.loc [:, cols].groupby('Order_Date').count().reset_index()
df_aux.head()

#desenhar gráfico de linhas
#plotly
import plotly.express as px
px.bar(df_aux, x='Order_Date',y='ID' )

#Barra Lateral Streamlit

st.header('Marketplace - Visão Entregadores')
image_path = 'Captura de tela 2025-11-26 164657.png'
image= Image.open(image_path)
st.sidebar.image(image, width=120)

st.sidebar.markdown ('# Cury Company')
st.sidebar.markdown ('## Fastest Delivery in Town')
st.sidebar.markdown ("""---""")

st.sidebar.markdown('## Selecione uma data limite')

data_slider=st.sidebar.slider( 'Até qual valor?', value=datetime (2022, 4, 13), min_value=datetime(2022, 2, 11),max_value=datetime(2022, 4, 6), format='DD-MM-YYYY')
                  

st.sidebar.markdown("""---""")

traffic_options=st.sidebar.multiselect('Quais as condiçoes do trânsito',['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown ("""---""")
st.sidebar.markdown ('### Powered by Evertinho')
#filtro de data
linhas_selecionadas = df1['Order_Date'] < data_slider
df1 = df1.loc[linhas_selecionadas,:]
#filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1=df1.loc[linhas_selecionadas,:]

#LAYOUT STREAMLIT

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '', ''])
with tab1:
    with st.container():
        st.title('Overall Metrics')
        
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            st.markdown('')
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            #A menor e maior idade dos entregadores
            
            col1.metric ( 'Maior idade', maior_idade)

        with col2:
            st.markdown('')
            #A menor e maior idade dos entregadores
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Menor de idade', menor_idade)
        with col3:
            st.markdown('')
            #A pior e a melhor condição de veículos.
            melhor_condition = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric('Melhor condição de veículos', melhor_condition)
           
        with col4:
            st.markdown('')
           
            col4.metric('Pior condição de veículos', df1.loc[:, 'Vehicle_condition'].min())
    with st.container():
        st.markdown("""---""")
        st.title('Avaliações')

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('Avaliações médias por Entregador')
            df_avg_delivery = (df1.loc[:, ['Delivery_person_ID','Delivery_person_Ratings']].groupby('Delivery_person_ID').mean().reset_index())
            st.dataframe (df_avg_delivery)

            
        with col2:
            st.markdown('Avaliação média por trânsito')
            #A avaliação média e o desvio padrão por tipo de tráfego.
            df_avg_traffic = df1.loc[:,['Delivery_person_Ratings','Road_traffic_density']].groupby('Road_traffic_density').agg({'Delivery_person_Ratings': ['mean','std']})
            df_avg_traffic.columns = ['Delivery_mean','Delivery_std']
            df_avg_traffic=df_avg_traffic.reset_index()
            st.dataframe (df_avg_traffic)
            
            
            st.markdown('Avaliação média por clima')
            #A avaliação média e o desvio padrão por condições climáticas.

            df1.loc[:,['Delivery_person_Ratings','Weatherconditions']]
            df_avg_weather = df1.loc[:, ['Delivery_person_Ratings','Weatherconditions']].groupby('Weatherconditions').agg({'Delivery_person_Ratings': ['mean','std']})
            df_avg_weather.columns = ['Delivery_mean','Delivery_std']
            df_avg_weather.reset_index()
            st.dataframe (df_avg_weather)

    with st.container():
        st.markdown("""---""")
        st.title('Velocidade de Entrega')

        col1, col2 = st.columns (2)
        with col1:
            st.markdown('Top entregadores mais rápidos')
                        #Os 10 entregadores mais rápidos por cidade.
            
            df2 = df1.loc[:,['Delivery_person_ID','City','Time_taken(min)']].groupby(['City','Delivery_person_ID']).min().sort_values(['City','Time_taken(min)'], ascending=True).reset_index()
            
            df3 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
            df4 = df2.loc[df2['City'] == 'Urban', :].head(10)
            df5 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
            df6 = pd.concat([df3,df4,df5]).reset_index(drop=True)
            st.dataframe (df6)
        with col2:
            st.markdown('Top entregadores mais lentos')
                        #Os 10 entregadores mais lentos por cidade.
            
            df2 = df1.loc[:,['Delivery_person_ID','City','Time_taken(min)']].groupby(['City','Delivery_person_ID']).max().sort_values(['City','Time_taken(min)'], ascending=False).reset_index()
            
            df3 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
            df4 = df2.loc[df2['City'] == 'Urban', :].head(10)
            df5 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
            df6 = pd.concat([df3,df4,df5]).reset_index(drop=True)
            st.dataframe(df6)

            
            
