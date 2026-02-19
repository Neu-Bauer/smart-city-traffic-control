const int PIN_RED_1 = 13;
const int PIN_YEL_1 = 12;
const int PIN_GRN_1 = 11;

const int PIN_RED_2 = 10;
const int PIN_YEL_2 = 9;
const int PIN_GRN_2 = 8;

unsigned long ultimoSinalPython = 0;
const unsigned long TEMPO_MAXIMO_ESPERA = 5000; 
bool modoBurroAtivado = true; 

unsigned long tempoUltimaTrocaBurra = 0;
int estadoBurro = 1; 

void setup() {
  Serial.begin(9600);
  
  pinMode(PIN_RED_1, OUTPUT);
  pinMode(PIN_YEL_1, OUTPUT);
  pinMode(PIN_GRN_1, OUTPUT);
  
  pinMode(PIN_RED_2, OUTPUT);
  pinMode(PIN_YEL_2, OUTPUT);
  pinMode(PIN_GRN_2, OUTPUT);

  apagarTudo();
}

void loop() {
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    int estadoPython = comando.toInt();
    
  
    if (estadoPython >= 1 && estadoPython <= 7) {
      ultimoSinalPython = millis(); 
      modoBurroAtivado = false;     
      aplicarLuzes(estadoPython);   
    }
  }
  if (millis() - ultimoSinalPython > TEMPO_MAXIMO_ESPERA) {
    modoBurroAtivado = true; 
  }

  if (modoBurroAtivado) {
    executarModoBurro();
  }
}

void aplicarLuzes(int estado) {
  apagarTudo(); 
  
  switch (estado) {
    case 1:
      digitalWrite(PIN_GRN_1, HIGH);
      digitalWrite(PIN_RED_2, HIGH);
      break;
    case 2:
      digitalWrite(PIN_YEL_1, HIGH);
      digitalWrite(PIN_RED_2, HIGH);
      break;
    case 3:
      digitalWrite(PIN_RED_1, HIGH);
      digitalWrite(PIN_RED_2, HIGH);
      break;
    case 4: 
      digitalWrite(PIN_RED_1, HIGH);
      digitalWrite(PIN_GRN_2, HIGH);
      break;
    case 5: 
      digitalWrite(PIN_RED_1, HIGH);
      digitalWrite(PIN_YEL_2, HIGH);
      break;
    case 6: 
      digitalWrite(PIN_RED_1, HIGH);
      digitalWrite(PIN_RED_2, HIGH);
      break;
    case 7:
      digitalWrite(PIN_YEL_1, HIGH);
      digitalWrite(PIN_YEL_2, HIGH);
      break;
  }
}

void apagarTudo() {
  digitalWrite(PIN_RED_1, LOW); digitalWrite(PIN_YEL_1, LOW); digitalWrite(PIN_GRN_1, LOW);
  digitalWrite(PIN_RED_2, LOW); digitalWrite(PIN_YEL_2, LOW); digitalWrite(PIN_GRN_2, LOW);
}

void executarModoBurro() {
  unsigned long agora = millis();
  unsigned long tempoDecorrido = agora - tempoUltimaTrocaBurra;

  
  if (estadoBurro == 1 && tempoDecorrido > 10000) { 
    estadoBurro = 2; tempoUltimaTrocaBurra = agora; 
  } 
  else if (estadoBurro == 2 && tempoDecorrido > 3000) { 
    estadoBurro = 3; tempoUltimaTrocaBurra = agora; 
  } 
  else if (estadoBurro == 3 && tempoDecorrido > 2000) { 
    estadoBurro = 4; tempoUltimaTrocaBurra = agora; 
  } 
  else if (estadoBurro == 4 && tempoDecorrido > 10000) { 
    estadoBurro = 5; tempoUltimaTrocaBurra = agora; 
  } 
  else if (estadoBurro == 5 && tempoDecorrido > 3000) { 
    estadoBurro = 6; tempoUltimaTrocaBurra = agora; 
  } 
  else if (estadoBurro == 6 && tempoDecorrido > 2000) { 
    estadoBurro = 1; tempoUltimaTrocaBurra = agora; 
  }

  aplicarLuzes(estadoBurro);
}