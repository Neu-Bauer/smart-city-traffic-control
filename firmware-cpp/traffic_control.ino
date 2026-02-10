// --- DEFINIÇÃO DOS PINOS (Hardware) ---
// VIA 1
const int V1_VERMELHO = 2;
const int V1_AMARELO  = 3;
const int V1_VERDE    = 4;

// VIA 2
const int V2_VERMELHO = 5;
const int V2_AMARELO  = 6;
const int V2_VERDE    = 7;

void setup() {
  // Inicia comunicação Serial (Mesma velocidade do Python: 9600)
  Serial.begin(9600);

  // Configura pinos como SAÍDA (Output)
  pinMode(V1_VERMELHO, OUTPUT);
  pinMode(V1_AMARELO, OUTPUT);
  pinMode(V1_VERDE, OUTPUT);
  
  pinMode(V2_VERMELHO, OUTPUT);
  pinMode(V2_AMARELO, OUTPUT);
  pinMode(V2_VERDE, OUTPUT);

  // Teste inicial: Pisca tudo 2 vezes para avisar que ligou
  piscarTudo();
}

void loop() {
  // Verifica se o Python mandou alguma mensagem
  if (Serial.available() > 0) {
    
    // Lê o número enviado (Lê até encontrar a quebra de linha '\n')
    int estadoRecebido = Serial.parseInt();

    // Joga fora qualquer lixo que sobrou no buffer
    Serial.read(); 

    // --- MÁQUINA DE ESTADOS (Hardware) ---
    // 1 a 6 são os códigos que definimos no Python
    switch (estadoRecebido) {
      case 1: // VIA 1 VERDE
        setSemaforo(1, false, false, true);  // V1: Verde
        setSemaforo(2, true, false, false);  // V2: Vermelho
        break;

      case 2: // VIA 1 AMARELO
        setSemaforo(1, false, true, false);  // V1: Amarelo
        setSemaforo(2, true, false, false);  // V2: Vermelho
        break;

      case 3: // SEGURANÇA 1 (AMBOS VERMELHOS)
        setSemaforo(1, true, false, false);
        setSemaforo(2, true, false, false);
        break;

      case 4: // VIA 2 VERDE
        setSemaforo(1, true, false, false);  // V1: Vermelho
        setSemaforo(2, false, false, true);  // V2: Verde
        break;
      
      case 5: // VIA 2 AMARELO
        setSemaforo(1, true, false, false);  // V1: Vermelho
        setSemaforo(2, false, true, false);  // V2: Amarelo
        break;

      case 6: // SEGURANÇA 2 (AMBOS VERMELHOS)
        setSemaforo(1, true, false, false);
        setSemaforo(2, true, false, false);
        break;
    }
  }
}

// --- FUNÇÕES AUXILIARES ---

// Função para controlar um semáforo específico (1 ou 2)
void setSemaforo(int via, bool r, bool y, bool g) {
  int pinoR, pinoY, pinoG;

  if (via == 1) {
    pinoR = V1_VERMELHO; pinoY = V1_AMARELO; pinoG = V1_VERDE;
  } else {
    pinoR = V2_VERMELHO; pinoY = V2_AMARELO; pinoG = V2_VERDE;
  }

  // digitalWrite: HIGH = Aceso (5V), LOW = Apagado (0V)
  digitalWrite(pinoR, r ? HIGH : LOW);
  digitalWrite(pinoY, y ? HIGH : LOW);
  digitalWrite(pinoG, g ? HIGH : LOW);
}

void piscarTudo() {
  for(int i=0; i<2; i++) {
    setSemaforo(1, 1, 1, 1); setSemaforo(2, 1, 1, 1);
    delay(200);
    setSemaforo(1, 0, 0, 0); setSemaforo(2, 0, 0, 0);
    delay(200);
  }
}