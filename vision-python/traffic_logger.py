import csv
import os
from datetime import datetime

class TrafficLogger:
    def __init__(self, filename="dados_tcc_trafego.csv"):
        self.filename = filename
        self._inicializar_arquivo()

    def _inicializar_arquivo(self):
        """Cria o arquivo com cabeçalhos se ele não existir."""
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow([
                    "Data_Hora", 
                    "Evento", 
                    "Fila_Via_1", 
                    "Fila_Via_2", 
                    "Decisao_Tomada",
                    "Tempo_Decorrido"
                ])
            print(f"--- [SISTEMA] Arquivo de Log criado: {self.filename} ---")

    def registrar_troca(self, fila1, fila2, decisao, tempo_decorrido):
        """Salva uma linha nova na planilha."""
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        with open(self.filename, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow([
                agora, 
                "TROCA_DE_SINAL", 
                fila1, 
                fila2, 
                decisao,
                f"{tempo_decorrido:.2f}s"
            ])
        print(f"   >>> [LOG SALVO] Decisão: {decisao} | Filas: {fila1} x {fila2}")