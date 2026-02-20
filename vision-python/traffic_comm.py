import serial
import time

class TrafficComm:
    def __init__(self, porta='COM3', baudrate=9600):
        """
        Inicializa a comunicação com o Arduino.
        Se não encontrar, entra em modo SIMULAÇÃO (Mock).
        """
        self.arduino = None
        self.modo_simulacao = False

        try:
            self.arduino = serial.Serial(porta, baudrate, timeout=1)
            time.sleep(2)
            print(f"✅ [COMM] Arduino conectado na porta {porta}")
        except serial.SerialException:
            self.modo_simulacao = True
            print(f"⚠️ [COMM] Arduino não encontrado em {porta}. Modo SIMULAÇÃO ativado.")

    def enviar_estado(self, estado_id):
        """Envia o número do estado (1 a 6) para o Arduino."""
        mensagem = str(estado_id) + '\n'
        
        if not self.modo_simulacao and self.arduino and self.arduino.is_open:
            self.arduino.write(mensagem.encode('utf-8'))
        else:
             print(f"[SERIAL MOCK] Enviando comando: {estado_id}")

    def fechar(self):
        if self.arduino and self.arduino.is_open:
            self.arduino.close()