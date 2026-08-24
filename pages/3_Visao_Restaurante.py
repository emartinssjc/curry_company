#titulo 
import io
import re
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from haversine import haversine
import streamlit as st
from datetime import datetime
from PIL import Image
import plotly.express as px
import folium
from streamlit_folium import folium_static
st.set_page_config(page_title = 'Visão Restaurantes', page_icon='XD', layout='wide')
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

st.header('Marketplace - Visão Restaurante')
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


tab1, tab2, tab3 = st.tabs(['Visão Restaurante', '', ''])
with tab1:
    with st.container():
        st.title("Overal Metrics")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
                        #A quantidade de entregadores únicos.
            delivery_unique = len (df1.loc[:, 'Delivery_person_ID'].unique())
            col1.metric ('Entregadores únicos', delivery_unique)
        with col2:
            col = ['Delivery_location_latitude','Restaurant_longitude', 'Restaurant_latitude','Delivery_location_longitude']
            df1['Distance'] = df1.loc[:,col].apply (lambda x: haversine((x['Restaurant_latitude'],x['Restaurant_longitude']), (x['Delivery_location_latitude'],x['Delivery_location_longitude'])), axis=1)
            avg_distance = np.round (df1['Distance'].mean(), 2)
            col2.metric ('Distância Média ', avg_distance)
        with col3:
            #O tempo médio de entrega durantes os Festivais.
    
            df_aux = df1.loc[:,['Time_taken(min)', 'Festival']].groupby('Festival').agg({'Time_taken(min)': ['mean','std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux=df_aux.reset_index()
            linhas_selecionadas = df_aux['Festival'] == 'Yes'
            df_aux =np.round ( df_aux.loc[linhas_selecionadas,'avg_time'], 2)
            col3.metric ('Tempo Médio Festival', df_aux)
        with col4:
            #O Desvio Padrão de entrega durantes os Festivais.
    
            df_aux = df1.loc[:,['Time_taken(min)', 'Festival']].groupby('Festival').agg({'Time_taken(min)': ['mean','std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux=df_aux.reset_index()
            linhas_selecionadas = df_aux['Festival'] == 'Yes'
            df_aux =np.round ( df_aux.loc[linhas_selecionadas,'std_time'], 2)
            col4.metric ('Desvio Padrão Festival', df_aux)

            
        with col5:
                 #O tempo médio de entrega sem ser nos Festivais.
    
            df_aux = df1.loc[:,['Time_taken(min)', 'Festival']].groupby('Festival').agg({'Time_taken(min)': ['mean','std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux=df_aux.reset_index()
            linhas_selecionadas = df_aux['Festival'] == 'No'
            df_aux =np.round ( df_aux.loc[linhas_selecionadas,'avg_time'], 2)
            col5.metric ('Tempo Médio sem Festival', df_aux)

        with col6:
              #O Desvio Padrão de entrega durantes os Festivais.
    
            df_aux = df1.loc[:,['Time_taken(min)', 'Festival']].groupby('Festival').agg({'Time_taken(min)': ['mean','std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux=df_aux.reset_index()
            linhas_selecionadas = df_aux['Festival'] == 'No'
            df_aux =np.round ( df_aux.loc[linhas_selecionadas,'std_time'], 2)
            col4.metric ('Desvio Padrão sem Festival', df_aux)
        
    with st.container():
        st.markdown("#### Tempo Médio de entrega por cidade")
        
        df1['Distance'] = df1.loc[:,['Delivery_location_latitude','Restaurant_longitude', 'Restaurant_latitude','Delivery_location_longitude']].apply (lambda x: haversine((x['Restaurant_latitude'],x['Restaurant_longitude']), (x['Delivery_location_latitude'],x['Delivery_location_longitude'])), axis=1)
        avg_distance = df1.loc[:,['City', 'Distance']].groupby('City').mean().reset_index()
        fig=go.Figure(data=[go.Pie(labels=avg_distance['City'], values = avg_distance['Distance'], pull=[0, 0.1, 0])])
        st.plotly_chart (fig)
        
    with st.container():
        st.markdown("#### Distribuição do Tempo")
        col1, col2 = st.columns(2)
        with col1:
            #O tempo médio e o desvio padrão de entrega por cidade e por tipo de pedido 
            cols = ['City','Time_taken(min)', 'Type_of_order']
            df_aux = df1.loc[:,cols].groupby(['City','Type_of_order']).agg({'Time_taken(min)': ['mean','std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            fig=go.Figure()
            fig.add_trace(go.Bar(name='Control', x=df_aux['City'], y=df_aux['avg_time'], error_y = dict (type='data', array=df_aux['std_time'])))
            fig.update_layout(barmode='group')
            st.plotly_chart(fig)
        with col2:
            cols = ['City','Time_taken(min)', 'Road_traffic_density']
            df_aux = df1.loc[:,cols].groupby(['City','Road_traffic_density']).agg({'Time_taken(min)': ['mean','std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()

            fig= px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values = 'avg_time', color='std_time', color_continuous_scale='RdBu', color_continuous_midpoint=np.average(df_aux['std_time']))
            st.plotly_chart(fig)
        
    with st.container():
        st.markdown("#### Distribuição da Distância")
        #O tempo médio e o desvio padrão de entrega por cidade e por tipo de pedido 
        cols = ['City','Time_taken(min)', 'Type_of_order']
        df_aux = df1.loc[:,cols].groupby(['City','Type_of_order']).agg({'Time_taken(min)': ['mean','std']})
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()
        st.dataframe(df_aux)
