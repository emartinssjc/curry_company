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
st.set_page_config(page_title = 'Visão Empresa', page_icon='XD', layout='wide')
df = pd.read_csv('train.csv')


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

st.header('Marketplace - Visão Cliente')
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

#Layout Streamlit
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    #Quantidade de pedidos por dia
    #colunas
    with st.container():
        st.header('Orders by Day')
        cols = ['ID', 'Order_Date']

    #linhas
        df_aux = df1.loc [:, cols].groupby('Order_Date').count().reset_index()
        df_aux.head()

    #desenhar gráfico de linhas
    #plotly
   
        fig = px.bar(df_aux, x='Order_Date',y='ID' )
        st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns (2)
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.header ('Traffic Order Share')
                #Distribuição dos pedidos por tipo de tráfego.
                df_aux = df1.loc [:, ['ID', 'Road_traffic_density']].groupby ('Road_traffic_density').count().reset_index()
                
                df_aux['entrega_perc'] = df_aux['ID'] / df_aux['ID'].sum()

                fig= px.pie(df_aux, values='entrega_perc', names='Road_traffic_density')
                st.plotly_chart(fig, use_container_width=True)

                
            with col2:
                 st.header ('Traffic Order City')
                #Comparação do volume de pedidos por cidade e tipo de tráfego.
                 df_aux = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
                 fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
                 st.plotly_chart(fig, use_container_width=True)

with tab3:
    
    #A localização central de cada cidade por tipo de tráfego.
    st.markdown("# Country Maps")
    df_aux = df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()

    df_aux = df_aux.head()
    map=folium.Map()
    for index, location_info in df_aux.iterrows():
        folium.Marker ([location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']], popup=location_info[['City', 'Road_traffic_density']]).add_to(map)
    folium_static(map, width= 1024, height=600)

with tab2:
    with st.container():
        st.markdown("# Order by Week")
        #Quantidade de pedidos por semana.
    #CRIAR A COLUNA DA SEMANA
    
        df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    
        df_aux = df1.loc[:,['ID', 'week_of_year'] ].groupby('week_of_year').count().reset_index()
        df_aux.head()
    
        fig=px.line(df_aux, x='week_of_year', y='ID')
        st.plotly_chart(fig, use_container_width = True)

    with st.container():
         st.markdown("# Order Share by Week")
                #A quantidade de pedidos por entregador por semana.
         df_aux01 = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
         df_aux02 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()
        
         df_aux = pd.merge(df_aux01, df_aux02, how='inner')
         df_aux['Order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
        
         fig = px.line(df_aux, x='week_of_year', y='Order_by_deliver')
         st.plotly_chart(fig, use_container_width = True)
