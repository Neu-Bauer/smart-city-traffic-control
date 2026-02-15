// --- DEFINIÇÃO DOS PINOS (Corrigida) ---
// VIA 1 (Esquerda)
const int V1_VERMELHO = 5;
const int V1_AMARELO  = 6;
const int V1_VERDE    = 7;

// VIA 2 (Direita)
const int V2_VERMELHO = 2;
const int V2_AMARELO  = 3;
const int V2_VERDE    = 4;
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
  
  // Aviso para forçar o Serial Monitor a abrir
  Serial.println("Arduino Pronto! Digite um estado (1 a 6):");
}

void loop() {
  // Verifica se o Python (ou você no terminal) mandou alguma mensagem
  if (Serial.available() > 0) {
    
    // Lê apenas 1 caractere por vez
    char comando = Serial.read();

    // Filtro de Segurança: Ignora o "Enter" invisível que o Wokwi manda (\n ou \r)
    if (comando == '\n' || comando == '\r' || comando == ' ') {
      return; 
    }

    // Converte o texto digitado para número matemático
    int estadoRecebido = comando - '0';

    // --- MÁQUINA DE ESTADOS (Hardware) ---
    switch (estadoRecebido) {
      case 1: // VIA 1 VERDE
        setSemaforo(1, false, false, true);  // V1: Verde
        setSemaforo(2, true, false, false);  // V2: Vermelho
        Serial.println("-> Comando 1: Via 1 VERDE / Via 2 VERMELHO");
        break;

      case 2: // VIA 1 AMARELO
        setSemaforo(1, false, true, false);  // V1: Amarelo
        setSemaforo(2, true, false, false);  // V2: Vermelho
        Serial.println("-> Comando 2: Via 1 AMARELO / Via 2 VERMELHO");
        break;

      case 3: // SEGURANÇA 1 (AMBOS VERMELHOS)
        setSemaforo(1, true, false, false);
        setSemaforo(2, true, false, false);
        Serial.println("-> Comando 3: AMBOS VERMELHOS (Seguranca)");
        break;

      case 4: // VIA 2 VERDE
        setSemaforo(1, true, false, false);  // V1: Vermelho
        setSemaforo(2, false, false, true);  // V2: Verde
        Serial.println("-> Comando 4: Via 1 VERMELHO / Via 2 VERDE");
        break;
      
      case 5: // VIA 2 AMARELO
        setSemaforo(1, true, false, false);  // V1: Vermelho
        setSemaforo(2, false, true, false);  // V2: Amarelo
        Serial.println("-> Comando 5: Via 1 VERMELHO / Via 2 AMARELO");
        break;

      case 6: // SEGURANÇA 2 (AMBOS VERMELHOS)
        setSemaforo(1, true, false, false);
        setSemaforo(2, true, false, false);
        Serial.println("-> Comando 6: AMBOS VERMELHOS (Seguranca)");
        break;
        
      default:
        Serial.println("-> Comando Invalido! Digite apenas de 1 a 6.");
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