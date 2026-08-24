import streamlit as srt
from PIL import Image

srt.set_page_config(page_title='Home', page_icon=':)')

#image_path='/Users/evert/Desktop/ANALISTA DE DADOS/PYTHON/PYTHON/Jupter_Lab/'
image=Image.open('Captura de tela 2025-11-26 164657.png')
srt.sidebar.image(image, width=120)



srt.sidebar.markdown ('# Cury Company')
srt.sidebar.markdown ('## Fastest Delivery in Town')
srt.sidebar.markdown ("""---""")

srt.write ('# Cury Company Dasboard')
srt.markdown(""" 
             Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
             ### Como utilizar esse Growth Dashboard?
             - Visão Empresa:
             - Visão Gerencias: Métricas gerais de comportamento.
             - Visão Tática: Indicadores semanais de crescimento.
             -Visão geográfica: Insigths de geolocalização.
             -Visão Entregador:
             -Acompanhamento dos indicadores semanais de crescimento 
             -Visão Restaurante:
             -Indicadores semanais de crescimento dos restaurantes 
             ### Ask for Help
             -Time de Data Science no Discord
             -@everton1882
             """)

                  



srt.sidebar.markdown ("""---""")
srt.sidebar.markdown ('### Powered by Evertinho')