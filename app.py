import streamlit as st
from weather_api import get_weather_data, get_forecast_data
import unicodedata
from datetime import datetime


API_KEY = "e74e06e41160ff6251fce0e8891351f7"


def remover_acentos(txt):
    return ''.join(c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn')

st.set_page_config(page_title="Previsão do Tempo", layout="centered")
st.title("🌦️ Previsão do Tempo")

# histórico na sessão
if "historico" not in st.session_state:
    st.session_state.historico = []

cidade = st.text_input("Digite o nome da cidade:")

if cidade:
    cidade_sem_acentos = remover_acentos(cidade)
    dados = get_weather_data(cidade_sem_acentos, API_KEY)
    
    cidade_formatada = cidade.title()  # Com inicial maiúscula
    if cidade_formatada not in st.session_state.historico:
        st.session_state.historico.append(cidade_formatada)

    # histórico de cidades buscadas
    st.sidebar.title("🔍 Cidades buscadas")
    for c in st.session_state.historico[::-1]:  # Mostra o mais recente no topo
        st.sidebar.write(f"• {c}")

    # Previsão para os próximos dias
    st.markdown("---")
    st.subheader("📅 Previsão para os próximos dias")

    forecast_data = get_forecast_data(cidade_sem_acentos, API_KEY)

    if forecast_data:
        dias_exibidos = []
        for item in forecast_data['list']:
            data_txt = item['dt_txt']
            data_obj = datetime.strptime(data_txt, "%Y-%m-%d %H:%M:%S")

            # Exibir previsão apenas às 12h de cada dia
            if data_obj.hour == 12 and data_obj.date() not in dias_exibidos:
                dias_exibidos.append(data_obj.date())
                temp = round(item['main']['temp'])
                desc = item['weather'][0]['description'].capitalize()
                icon = item['weather'][0]['icon']
                icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"

                with st.container():
                    st.write(f"📅 {data_obj.strftime('%d/%m (%a)')} - {desc} - {temp} °C")
                    st.image(icon_url, width=60)

    if dados:
        st.subheader(f"📍 {dados['name']}, {dados['sys']['country']}")
        icon_code = dados['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        st.image(icon_url)
        
        # Clima principal em texto
        st.write(f"☁️ Clima: {dados['weather'][0]['description'].capitalize()}")

        # Métricas organizadas lado a lado
        col1, col2, col3 = st.columns(3)
        col1.metric("🌡️ Temperatura", f"{round(dados['main']['temp'])} °C")
        col2.metric("💧 Umidade", f"{dados['main']['humidity']}%")
        col3.metric("💨 Vento", f"{dados['wind']['speed']} m/s")

        st.caption(f"🕒 Dados atualizados em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    else:
        st.error("Não foi possível obter os dados. Verifique o nome da cidade ou sua conexão.")
