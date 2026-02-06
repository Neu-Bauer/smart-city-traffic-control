import cv2
import numpy as np
from ultralytics import YOLO

# Importando nossos Módulos Profissionais
from traffic_logger import TrafficLogger
from traffic_controller import TrafficController

# --- CONFIGURAÇÃO ---
VIDEO_SOURCE = 'teste.mp4' # Ou 0 para webcam
ZONA_1 = np.array([[782, 477], [863, 487], [1268, 996], [6, 986]], np.int32)
ZONA_2 = np.array([[948, 495], [1086, 472], [1893, 838], [1356, 996]], np.int32)

# Cores (BGR)
COR_AMARELO = (0, 255, 255)
COR_MAGENTA = (255, 0, 255)
COR_VERDE_LUZ = (0, 255, 0)
COR_VERMELHO_LUZ = (0, 0, 255)
COR_AMARELO_LUZ = (0, 255, 255)
COR_DESLIGADO = (50, 50, 50)

def main():
    # 1. Inicializa Sistemas
    logger = TrafficLogger()
    controlador = TrafficController()
    
    # Conecta o Logger ao Controlador (Design Pattern: Callback)
    # Sempre que o controlador decidir trocar, ele avisa o logger automaticamente
    controlador.set_logger_callback(logger.registrar_troca)

    model = YOLO('yolov8n.pt')
    cap = cv2.VideoCapture(VIDEO_SOURCE)

    print("--- SISTEMA INICIADO ---")

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # Loop infinito
            continue

        # 2. Visão Computacional (Input)
        results = model(frame, stream=True, classes=[2, 5, 7], conf=0.3, verbose=False)
        
        fila_v1 = 0
        fila_v2 = 0

        # Desenha as zonas
        cv2.polylines(frame, [ZONA_1], isClosed=True, color=COR_AMARELO, thickness=2)
        cv2.polylines(frame, [ZONA_2], isClosed=True, color=COR_MAGENTA, thickness=2)

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cx, cy = int((x1+x2)/2), int((y1+y2)/2)

                # Verifica em qual zona está
                if cv2.pointPolygonTest(ZONA_1, (cx, cy), False) >= 0:
                    fila_v1 += 1
                    cv2.rectangle(frame, (x1, y1), (x2, y2), COR_AMARELO, 2)
                elif cv2.pointPolygonTest(ZONA_2, (cx, cy), False) >= 0:
                    fila_v2 += 1
                    cv2.rectangle(frame, (x1, y1), (x2, y2), COR_MAGENTA, 2)

        # 3. Lógica de Controle (Processing)
        # O main apenas entrega os dados e pergunta: "E agora?"
        controlador.atualizar(fila_v1, fila_v2)
        
        # Pega o estado das luzes para desenhar
        luzes_v1, luzes_v2 = controlador.get_luzes()

        # 4. Interface Gráfica (Output)
        desenhar_painel(frame, 50, 50, luzes_v1, fila_v1, "VIA 1", COR_AMARELO)
        desenhar_painel(frame, 50, 150, luzes_v2, fila_v2, "VIA 2", COR_MAGENTA)

        cv2.imshow("Smart City Traffic Control", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def desenhar_painel(img, x, y, luzes, fila, nome, cor_texto):
    """Função auxiliar para desenhar o semáforo bonito"""
    vermelho, amarelo, verde = luzes
    
    # Define as cores finais (Aceso ou Apagado)
    c_r = COR_VERMELHO_LUZ if vermelho else COR_DESLIGADO
    c_y = COR_AMARELO_LUZ if amarelo else COR_DESLIGADO
    c_g = COR_VERDE_LUZ if verde else COR_DESLIGADO

    # Desenha caixa e luzes
    cv2.rectangle(img, (x-10, y-10), (x+30, y+80), (0,0,0), -1)
    cv2.circle(img, (x+10, y+10), 8, c_r, -1)
    cv2.circle(img, (x+10, y+35), 8, c_y, -1)
    cv2.circle(img, (x+10, y+60), 8, c_g, -1)
    
    # Texto
    cv2.putText(img, f'{nome}: {fila}', (x+40, y+45), cv2.FONT_HERSHEY_SIMPLEX, 0.8, cor_texto, 2)

if __name__ == "__main__":
    main()