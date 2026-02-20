import cv2
import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from ultralytics import YOLO

from traffic_logger import TrafficLogger
from traffic_controller import TrafficController
from traffic_comm import TrafficComm

st.set_page_config(page_title="TCC - Smart City", layout="wide", initial_sidebar_state="expanded")

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2085/2085392.png", width=100)
    st.title("Painel de Controle")
    st.markdown("Controle mestre do sistema de visão computacional.")
    st.markdown("---")
    
    modo_noturno = st.toggle(" Modo Noturno (Intermitente)", value=False)
    
    st.markdown("---")
    stop_button = st.button(" PARAR SISTEMA", use_container_width=True)
    st.markdown("---")
    st.caption("Desenvolvido para TCC de Engenharia de Software")

st.title(" Monitoramento de Tráfego - CCO")
st.markdown("Processamento de fluxo em tempo real com YOLOv8 e controle de estados.")
st.markdown("---")

aba_ao_vivo, aba_relatorios = st.tabs(["Visão ao Vivo", "Relatórios de Eficiência"])

ARQUIVO_CSV = 'dados_tcc_trafego.csv'

with aba_relatorios:
    st.header("Análise Histórica do Sistema")
    
    if os.path.exists(ARQUIVO_CSV):
        try:
            df = pd.read_csv(ARQUIVO_CSV, sep=None, engine='python', names=['Timestamp', 'Fila_V1', 'Fila_V2', 'Motivo', 'Tempo_Verde'], header=0)
            df['Tempo_Verde'] = df['Tempo_Verde'].astype(str).str.replace('s', '', regex=False).astype(float)
            
            df['Fila_V1'] = pd.to_numeric(df['Fila_V1'], errors='coerce').fillna(0)
            df['Fila_V2'] = pd.to_numeric(df['Fila_V2'], errors='coerce').fillna(0)
            
            df['Fila_V1'] = df['Fila_V1'].apply(lambda x: 0 if x > 100 else x)
            df['Fila_V2'] = df['Fila_V2'].apply(lambda x: 0 if x > 100 else x)

            intervencoes = range(1, len(df) + 1)
            
            plt.style.use('ggplot')

            st.markdown("#### Volume de Veículos no Momento da Troca de Semáforo")
            fig1, ax1 = plt.subplots(figsize=(10, 4))
            ax1.plot(intervencoes, df['Fila_V1'], label='Via 1 (Carros)', color='#facc15', marker='o')
            ax1.plot(intervencoes, df['Fila_V2'], label='Via 2 (Carros)', color='#d946ef', marker='o')
            ax1.set_xlabel('Número da Intervenção')
            ax1.set_ylabel('Quantidade de Veículos')
            ax1.legend()
            ax1.grid(True, linestyle='--', alpha=0.7)
            st.pyplot(fig1)
            st.markdown("---")

            st.markdown("#### Variação do Tempo de Sinal Verde (Tempo Dinâmico)")
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            ax2.bar(intervencoes, df['Tempo_Verde'], color='#3b82f6', alpha=0.8)
            media_tempo = df['Tempo_Verde'].mean()
            ax2.axhline(y=media_tempo, color='red', linestyle='--', label=f'Média: {media_tempo:.1f}s')
            ax2.set_xlabel('Número da Intervenção')
            ax2.set_ylabel('Tempo em Segundos (s)')
            ax2.legend()
            st.pyplot(fig2)
            st.markdown("---")

            st.markdown("#### Distribuição dos Motivos de Troca")
            fig3, ax3 = plt.subplots(figsize=(6, 6))
            contagem_motivos = df['Motivo'].value_counts()
            ax3.pie(contagem_motivos, labels=contagem_motivos.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
            
            col_vazia1, col_grafico, col_vazia2 = st.columns([1, 2, 1])
            with col_grafico:
                st.pyplot(fig3)

        except Exception as e:
            st.error(f"Erro ao processar os dados do CSV: {e}")
    else:
        st.info("Nenhum dado encontrado. O sistema precisa rodar para gerar os primeiros registros.")

with aba_ao_vivo:
    col_video, col_painel = st.columns([2, 1.2])

    with col_video:
        video_placeholder = st.empty() 

    with col_painel:
        st.markdown("### Status das Vias")
        
        col_v1, col_v2 = st.columns(2)
        card_v1 = col_v1.empty()
        card_v2 = col_v2.empty()
        
        st.markdown("---")
        st.markdown("### Semáforo Atual")
        card_status = st.empty()

VIDEO_SOURCE = 'teste.mp4' 
ZONA_1 = np.array([[782, 477], [863, 487], [1268, 996], [6, 986]], np.int32)
ZONA_2 = np.array([[948, 495], [1086, 472], [1893, 838], [1356, 996]], np.int32)
COR_AMARELO = (0, 255, 255)
COR_MAGENTA = (255, 0, 255)
COR_EMERGENCIA = (0, 0, 255)

@st.cache_resource
def carregar_modelo():
    return YOLO('yolov8n.pt')

def main():
    logger = TrafficLogger()
    controlador = TrafficController()
    comm = TrafficComm(porta='COM3')
    controlador.set_logger_callback(logger.registrar_troca)

    controlador.forcar_modo_intermitente(modo_noturno)

    model = carregar_modelo()
    cap = cv2.VideoCapture(VIDEO_SOURCE)

    while cap.isOpened() and not stop_button:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        results = model(frame, stream=True, classes=[2, 5, 7], conf=0.3, imgsz=320, verbose=False)
        
        fila_v1, fila_v2 = 0, 0
        emergencia_v1, emergencia_v2 = 0, 0

        cv2.polylines(frame, [ZONA_1], isClosed=True, color=COR_AMARELO, thickness=2)
        cv2.polylines(frame, [ZONA_2], isClosed=True, color=COR_MAGENTA, thickness=2)

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cx, cy = int((x1+x2)/2), int((y1+y2)/2)
                classe_id = int(box.cls[0]) 
                is_emergency = (classe_id == 5 or classe_id == 7)

                if cv2.pointPolygonTest(ZONA_1, (cx, cy), False) >= 0:
                    if is_emergency:
                        emergencia_v1 += 1
                        cv2.rectangle(frame, (x1, y1), (x2, y2), COR_EMERGENCIA, 3)
                        cv2.putText(frame, "EMERGENCIA", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, COR_EMERGENCIA, 2)
                    else:
                        fila_v1 += 1
                        cv2.rectangle(frame, (x1, y1), (x2, y2), COR_AMARELO, 2)
                        
                elif cv2.pointPolygonTest(ZONA_2, (cx, cy), False) >= 0:
                    if is_emergency:
                        emergencia_v2 += 1
                        cv2.rectangle(frame, (x1, y1), (x2, y2), COR_EMERGENCIA, 3)
                        cv2.putText(frame, "EMERGENCIA", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, COR_EMERGENCIA, 2)
                    else:
                        fila_v2 += 1
                        cv2.rectangle(frame, (x1, y1), (x2, y2), COR_MAGENTA, 2)

        if emergencia_v1 > 0:
            fila_v1 = 999 
            fila_v2 = 0
            cv2.putText(frame, "[ ALERTA ] PRIORIDADE VIA 1", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, COR_EMERGENCIA, 3)
        elif emergencia_v2 > 0:
            fila_v1 = 0
            fila_v2 = 999 
            cv2.putText(frame, "[ ALERTA ] PRIORIDADE VIA 2", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, COR_EMERGENCIA, 3)

        estado_atual = controlador.atualizar(fila_v1, fila_v2)
        comm.enviar_estado(estado_atual)

        if controlador.modo_operacao == controlador.MODO_INTERMITENTE:
            txt_v1 = "INTERMITENTE"
            txt_v2 = "INTERMITENTE"
            card_status.warning("MODO NOTURNO (Amarelo Piscante)")
        else:
            txt_v1 = "ALERTA" if fila_v1 == 999 else str(fila_v1)
            txt_v2 = "ALERTA" if fila_v2 == 999 else str(fila_v2)
            
            if estado_atual == 1:
                card_status.success("🟢 VIA 1 ABERTA")
            elif estado_atual == 4:
                card_status.success("🟢 VIA 2 ABERTA")
            elif estado_atual in [3, 6]:
                card_status.error("🔴 MODO DE SEGURANÇA (Ambos Vermelhos)")
            else:
                card_status.warning("🟡 ATENÇÃO (Trocando Sinal)")

        card_v1.metric("Via 1 (Amarelo)", txt_v1)
        card_v2.metric("Via 2 (Magenta)", txt_v2)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        altura, largura = frame_rgb.shape[:2]
        frame_reduzido = cv2.resize(frame_rgb, (largura // 2, altura // 2))
        
        video_placeholder.image(frame_reduzido, channels="RGB", use_container_width=True)

    cap.release()

if __name__ == "__main__":
    main()