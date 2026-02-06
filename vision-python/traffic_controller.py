import time

class TrafficController:
    # Constantes de Estado (Enumeração simples)
    VIA_1_VERDE    = 1
    VIA_1_AMARELO  = 2
    SEGURANCA_1    = 3
    VIA_2_VERDE    = 4
    VIA_2_AMARELO  = 5
    SEGURANCA_2    = 6

    def __init__(self, tempo_min_verde=3.0, tempo_amarelo=2.0, tempo_seguranca=1.0):
        # Configurações
        self.TEMPO_MIN_VERDE = tempo_min_verde
        self.TEMPO_AMARELO = tempo_amarelo
        self.TEMPO_SEGURANCA = tempo_seguranca
        
        # Estado Inicial
        self.estado_atual = self.VIA_1_VERDE
        self.ultima_troca = time.time()
        
        # Memória para logs (quem vamos notificar quando trocar)
        self.logger_callback = None

    def set_logger_callback(self, callback_function):
        """Permite conectar o Logger a este controlador"""
        self.logger_callback = callback_function

    def atualizar(self, fila_via_1, fila_via_2):
        """
        Método principal: Recebe o tamanho das filas e decide se troca de estado.
        Retorna: O estado atual (após processamento).
        """
        tempo_decorrido = time.time() - self.ultima_troca
        novo_estado = self.estado_atual # Assume que nada muda por padrão

        # --- LÓGICA DA MÁQUINA DE ESTADOS ---
        
        # FASE 1: Via 1 está VERDE
        if self.estado_atual == self.VIA_1_VERDE:
            # Regra: Passou tempo min E fila 2 é maior que fila 1
            if tempo_decorrido > self.TEMPO_MIN_VERDE and fila_via_2 > fila_via_1:
                novo_estado = self.VIA_1_AMARELO
                self._notificar_troca(fila_via_1, fila_via_2, "Prioridade Via 2 (Fila Maior)", tempo_decorrido)

        # FASE 2: Via 1 AMARELO -> Vermelho
        elif self.estado_atual == self.VIA_1_AMARELO:
            if tempo_decorrido > self.TEMPO_AMARELO:
                novo_estado = self.SEGURANCA_1

        # FASE 3: Vermelho Segurança -> Via 2 VERDE
        elif self.estado_atual == self.SEGURANCA_1:
            if tempo_decorrido > self.TEMPO_SEGURANCA:
                novo_estado = self.VIA_2_VERDE

        # FASE 4: Via 2 está VERDE
        elif self.estado_atual == self.VIA_2_VERDE:
            if tempo_decorrido > self.TEMPO_MIN_VERDE and fila_via_1 > fila_via_2:
                novo_estado = self.VIA_2_AMARELO
                self._notificar_troca(fila_via_1, fila_via_2, "Prioridade Via 1 (Fila Maior)", tempo_decorrido)

        # FASE 5: Via 2 AMARELO -> Vermelho
        elif self.estado_atual == self.VIA_2_AMARELO:
            if tempo_decorrido > self.TEMPO_AMARELO:
                novo_estado = self.SEGURANCA_2

        # FASE 6: Vermelho Segurança -> Via 1 VERDE
        elif self.estado_atual == self.SEGURANCA_2:
            if tempo_decorrido > self.TEMPO_SEGURANCA:
                novo_estado = self.VIA_1_VERDE

        # Aplica a mudança se houve
        if novo_estado != self.estado_atual:
            self.estado_atual = novo_estado
            self.ultima_troca = time.time()

        return self.estado_atual

    def _notificar_troca(self, f1, f2, motivo, tempo):
        """Função interna para chamar o logger se ele estiver conectado"""
        if self.logger_callback:
            self.logger_callback(f1, f2, motivo, tempo)

    def get_luzes(self):
        """Retorna o estado das luzes para quem for desenhar na tela"""
        # Formato: (R1, Y1, G1), (R2, Y2, G2) - Onde True é Aceso
        
        # Padrão: Tudo Vermelho
        luzes_v1 = [True, False, False] 
        luzes_v2 = [True, False, False]

        if self.estado_atual == self.VIA_1_VERDE:
            luzes_v1 = [False, False, True] # Verde
        elif self.estado_atual == self.VIA_1_AMARELO:
            luzes_v1 = [False, True, False] # Amarelo

        if self.estado_atual == self.VIA_2_VERDE:
            luzes_v2 = [False, False, True] # Verde
        elif self.estado_atual == self.VIA_2_AMARELO:
            luzes_v2 = [False, True, False] # Amarelo
            
        return luzes_v1, luzes_v2