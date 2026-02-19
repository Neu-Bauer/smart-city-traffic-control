import time

class TrafficController:
    # Constantes de Estado do Semáforo
    VIA_1_VERDE    = 1
    VIA_1_AMARELO  = 2
    SEGURANCA_1    = 3  # Ambos vermelhos
    VIA_2_VERDE    = 4
    VIA_2_AMARELO  = 5
    SEGURANCA_2    = 6  # Ambos vermelhos
    INTERMITENTE   = 7  # NOVO: Amarelo piscante para os dois lados

    # Modos de Operação do Sistema (O "Override" Manual)
    MODO_AUTOMATICO = "AUTO"
    MODO_INTERMITENTE = "INTERMITENTE"

    def __init__(self, tempo_min_verde=10.0, tempo_amarelo=3.0, tempo_seguranca=2.0):
        # 1. Configurações de Tempo (Ajustados para mais realismo)
        self.TEMPO_MIN_VERDE = tempo_min_verde
        self.TEMPO_AMARELO = tempo_amarelo
        self.TEMPO_SEGURANCA = tempo_seguranca
        self.TEMPO_MAX_ESPERA = 30.0 # Se a rua vazia esperar 30s, o sinal abre para ela
        
        # 2. Configurações de Densidade de Fila (A SUA LÓGICA!)
        self.FILA_MINIMA = 3 # Só abre se a outra rua tiver pelo menos 3 carros
        self.FILA_MAXIMA = 8 # Se bater 8 carros, FORÇA a abertura imediatamente
        
        # 3. Estado Inicial
        self.estado_atual = self.VIA_1_VERDE
        self.modo_operacao = self.MODO_AUTOMATICO
        self.ultima_troca = time.time()
        self.inicio_espera = time.time() # Cronômetro para o carro da madrugada
        
        self.logger_callback = None

    def set_logger_callback(self, callback_function):
        self.logger_callback = callback_function

    def forcar_modo_intermitente(self, ativar: bool):
        """Função para o Dashboard ativar/desativar o Amarelo Piscante da madrugada"""
        if ativar:
            self.modo_operacao = self.MODO_INTERMITENTE
            self.estado_atual = self.INTERMITENTE
        else:
            self.modo_operacao = self.MODO_AUTOMATICO
            self.estado_atual = self.VIA_1_VERDE # Volta ao normal
            self.ultima_troca = time.time()

    def atualizar(self, fila_via_1, fila_via_2):
        """
        O CÉREBRO ADAPTATIVO: Avalia limites mínimos, máximos e tempos.
        """
        # Se a prefeitura ativou o modo noturno, ignora tudo e retorna amarelo piscante.
        if self.modo_operacao == self.MODO_INTERMITENTE:
            return self.INTERMITENTE

        tempo_decorrido = time.time() - self.ultima_troca
        tempo_esperando = time.time() - self.inicio_espera
        
        # Variável auxiliar para sabermos se devemos trocar o sinal ou não
        deve_trocar = False
        motivo_troca = ""

        # ==========================================
        # A MATEMÁTICA DE TRANSIÇÃO (Onde a mágica acontece)
        # ==========================================
        
        # 1. Analisando a VIA 1 (se ela está VERDE)
        if self.estado_atual == self.VIA_1_VERDE:
            # Regra de Segurança: Só analisa troca se já passou o Tempo Mínimo de Verde
            if tempo_decorrido > self.TEMPO_MIN_VERDE:
                
                # Regra 1: Caos na Via 2 (Fila Máxima Atingida)
                if fila_via_2 >= self.FILA_MAXIMA:
                    deve_trocar = True
                    motivo_troca = "Limite Maximo Atingido (Via 2)"
                
                # Regra 2: Eficiência (Via 2 atingiu o mínimo aceitável E é maior que a Via 1)
                elif fila_via_2 >= self.FILA_MINIMA and fila_via_2 > fila_via_1:
                    deve_trocar = True
                    motivo_troca = "Fluxo Normal Otimizado (Via 2 > Via 1)"
                
                # Regra 3: O Carro da Madrugada (Tem gente na Via 2 esperando tempo demais)
                elif fila_via_2 > 0 and tempo_esperando > self.TEMPO_MAX_ESPERA:
                    deve_trocar = True
                    motivo_troca = "Tempo Maximo de Espera (Via 2)"

            # Se alguma regra bateu, inicia o Amarelo!
            if deve_trocar:
                self.estado_atual = self.VIA_1_AMARELO
                self._notificar_troca(fila_via_1, fila_via_2, motivo_troca, tempo_decorrido)
                self.ultima_troca = time.time()

        # 2. Analisando a VIA 2 (se ela está VERDE)
        elif self.estado_atual == self.VIA_2_VERDE:
            if tempo_decorrido > self.TEMPO_MIN_VERDE:
                
                if fila_via_1 >= self.FILA_MAXIMA:
                    deve_trocar = True
                    motivo_troca = "Limite Maximo Atingido (Via 1)"
                    
                elif fila_via_1 >= self.FILA_MINIMA and fila_via_1 > fila_via_2:
                    deve_trocar = True
                    motivo_troca = "Fluxo Normal Otimizado (Via 1 > Via 2)"
                    
                elif fila_via_1 > 0 and tempo_esperando > self.TEMPO_MAX_ESPERA:
                    deve_trocar = True
                    motivo_troca = "Tempo Maximo de Espera (Via 1)"

            if deve_trocar:
                self.estado_atual = self.VIA_2_AMARELO
                self._notificar_troca(fila_via_1, fila_via_2, motivo_troca, tempo_decorrido)
                self.ultima_troca = time.time()

        # ==========================================
        # TEMPORIZADORES DE SEGURANÇA (Amarelo e Vermelho)
        # ==========================================
        
        # Transição Via 1 (Amarelo -> Vermelho)
        elif self.estado_atual == self.VIA_1_AMARELO:
            if tempo_decorrido > self.TEMPO_AMARELO:
                self.estado_atual = self.SEGURANCA_1
                self.ultima_troca = time.time()

        # Segurança (Vermelho -> Via 2 Verde)
        elif self.estado_atual == self.SEGURANCA_1:
            if tempo_decorrido > self.TEMPO_SEGURANCA:
                self.estado_atual = self.VIA_2_VERDE
                self.ultima_troca = time.time()
                self.inicio_espera = time.time() # Reseta o timer de quem tá esperando na Via 1

        # Transição Via 2 (Amarelo -> Vermelho)
        elif self.estado_atual == self.VIA_2_AMARELO:
            if tempo_decorrido > self.TEMPO_AMARELO:
                self.estado_atual = self.SEGURANCA_2
                self.ultima_troca = time.time()

        # Segurança (Vermelho -> Via 1 Verde)
        elif self.estado_atual == self.SEGURANCA_2:
            if tempo_decorrido > self.TEMPO_SEGURANCA:
                self.estado_atual = self.VIA_1_VERDE
                self.ultima_troca = time.time()
                self.inicio_espera = time.time() # Reseta o timer de quem tá esperando na Via 2

        return self.estado_atual

    def _notificar_troca(self, f1, f2, motivo, tempo):
        if self.logger_callback:
            self.logger_callback(f1, f2, motivo, tempo)

    def get_luzes(self):
        # ... (O código das luzes continua o mesmo) ...
        luzes_v1 = [True, False, False] 
        luzes_v2 = [True, False, False]

        if self.estado_atual == self.VIA_1_VERDE:
            luzes_v1 = [False, False, True]
        elif self.estado_atual == self.VIA_1_AMARELO:
            luzes_v1 = [False, True, False]

        if self.estado_atual == self.VIA_2_VERDE:
            luzes_v2 = [False, False, True]
        elif self.estado_atual == self.VIA_2_AMARELO:
            luzes_v2 = [False, True, False]
            
        # Para o modo noturno (os dois amarelos acessos pro painel)
        if self.estado_atual == self.INTERMITENTE:
             luzes_v1 = [False, True, False]
             luzes_v2 = [False, True, False]

        return luzes_v1, luzes_v2