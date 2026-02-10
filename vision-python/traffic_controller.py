import time

class TrafficController:
    # Constantes de Estado (Enumeração para facilitar a leitura)
    VIA_1_VERDE    = 1
    VIA_1_AMARELO  = 2
    SEGURANCA_1    = 3  # Ambos vermelhos antes de abrir a Via 2
    VIA_2_VERDE    = 4
    VIA_2_AMARELO  = 5
    SEGURANCA_2    = 6  # Ambos vermelhos antes de abrir a Via 1

    def __init__(self, tempo_min_verde=3.0, tempo_amarelo=2.0, tempo_seguranca=1.0):
        # Configurações de Tempo
        self.TEMPO_MIN_VERDE = tempo_min_verde
        self.TEMPO_AMARELO = tempo_amarelo
        self.TEMPO_SEGURANCA = tempo_seguranca
        
        # Estado Inicial
        self.estado_atual = self.VIA_1_VERDE
        self.ultima_troca = time.time()
        
        # Callback para Logs (quem avisar quando trocar o sinal)
        self.logger_callback = None

    def set_logger_callback(self, callback_function):
        """Conecta o sistema de logs a este controlador."""
        self.logger_callback = callback_function

    def atualizar(self, fila_via_1, fila_via_2):
        """
        O CÉREBRO: Recebe as filas atuais e decide se deve mudar de estado.
        """
        tempo_decorrido = time.time() - self.ultima_troca
        novo_estado = self.estado_atual # Assume que mantém o estado, a menos que...

        # --- LÓGICA DA MÁQUINA DE ESTADOS ---
        
        # 1. Se Via 1 está VERDE
        if self.estado_atual == self.VIA_1_VERDE:
            # Só troca se: Passou tempo mínimo E a outra via está pior
            if tempo_decorrido > self.TEMPO_MIN_VERDE and fila_via_2 > fila_via_1:
                novo_estado = self.VIA_1_AMARELO
                self._notificar_troca(fila_via_1, fila_via_2, "Prioridade Via 2 (Fila Maior)", tempo_decorrido)

        # 2. Transição Via 1 (Amarelo -> Vermelho)
        elif self.estado_atual == self.VIA_1_AMARELO:
            if tempo_decorrido > self.TEMPO_AMARELO:
                novo_estado = self.SEGURANCA_1

        # 3. Segurança (Vermelho -> Via 2 Verde)
        elif self.estado_atual == self.SEGURANCA_1:
            if tempo_decorrido > self.TEMPO_SEGURANCA:
                novo_estado = self.VIA_2_VERDE

        # 4. Se Via 2 está VERDE
        elif self.estado_atual == self.VIA_2_VERDE:
            if tempo_decorrido > self.TEMPO_MIN_VERDE and fila_via_1 > fila_via_2:
                novo_estado = self.VIA_2_AMARELO
                self._notificar_troca(fila_via_1, fila_via_2, "Prioridade Via 1 (Fila Maior)", tempo_decorrido)

        # 5. Transição Via 2 (Amarelo -> Vermelho)
        elif self.estado_atual == self.VIA_2_AMARELO:
            if tempo_decorrido > self.TEMPO_AMARELO:
                novo_estado = self.SEGURANCA_2

        # 6. Segurança (Vermelho -> Via 1 Verde)
        elif self.estado_atual == self.SEGURANCA_2:
            if tempo_decorrido > self.TEMPO_SEGURANCA:
                novo_estado = self.VIA_1_VERDE

        # Aplica a mudança
        if novo_estado != self.estado_atual:
            self.estado_atual = novo_estado
            self.ultima_troca = time.time()

        return self.estado_atual

    def _notificar_troca(self, f1, f2, motivo, tempo):
        """Função interna para chamar o logger se ele existir"""
        if self.logger_callback:
            # Chama a função registrar_troca lá do outro arquivo
            self.logger_callback(f1, f2, motivo, tempo)

    def get_luzes(self):
        """Retorna quais luzes devem estar acesas para desenhar na tela"""
        # Formato: [Vermelho, Amarelo, Verde] - True/False
        luzes_v1 = [True, False, False] # Padrão Vermelho
        luzes_v2 = [True, False, False]

        # Configura Via 1
        if self.estado_atual == self.VIA_1_VERDE:
            luzes_v1 = [False, False, True]
        elif self.estado_atual == self.VIA_1_AMARELO:
            luzes_v1 = [False, True, False]

        # Configura Via 2
        if self.estado_atual == self.VIA_2_VERDE:
            luzes_v2 = [False, False, True]
        elif self.estado_atual == self.VIA_2_AMARELO:
            luzes_v2 = [False, True, False]
            
        return luzes_v1, luzes_v2