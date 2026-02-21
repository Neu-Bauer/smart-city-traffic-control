# Smart City Traffic Control (Hybrid IoT System)

Status: Fase de Arquitetura de Software e Interface Web Concluídas. Iniciando etapa de prototipagem física.

Um sistema de gestão de tráfego inteligente que une a facilidade do Python para Inteligência Artificial com a performance do C++ para controle de hardware. O projeto utiliza câmeras para analisar o fluxo de veículos, otimizar o tempo de semáforos e apresentar dados estatísticos em um Dashboard de Centro de Controle Operacional (CCO) em tempo real.

## Principais Funcionalidades (Engenharia de Software)

Este projeto vai além da simples contagem de veículos, aplicando conceitos de sistemas de missão crítica:

* **Controle Adaptativo por Limiares (Thresholds):** O semáforo não utiliza tempos fixos. A máquina de estados toma decisões baseadas em densidade de tráfego, respeitando limites de eficiência (fila mínima) e limites críticos (fila máxima para escoamento), eliminando o "efeito ping-pong".
* **Tolerância a Falhas (Fail-Safe / Watchdog):** O firmware do hardware (C++) possui um mecanismo de "Cão de Guarda". Se o servidor principal (Python/IA) travar ou a conexão falhar, o cruzamento entra automaticamente em um modo autônomo temporizado de segurança (Degradação Graciosa).
* **Prioridade de Emergência:** O modelo de Visão Computacional detecta veículos prioritários, executando um *override* na lógica normal e forçando a liberação imediata da via.
* **Sobrescrita Manual (Override):** O Dashboard web possui um comando de "Modo Noturno", permitindo que operadores humanos assumam o controle e forcem o estado de Amarelo Intermitente.
* **Business Intelligence (BI) Integrado:** O sistema registra o histórico de trocas e renderiza, nativamente no Dashboard, relatórios estatísticos (Matplotlib/Pandas) provando a eficiência do tempo dinâmico contra o tempo estático.

## Arquitetura da Solução

O sistema opera em uma arquitetura híbrida de Mestre-Escravo via comunicação Serial:

### 1. Servidor CCO (Cérebro - Python)
* **Linguagem:** Python 3.x
* **Função:** * Captura imagens das câmeras urbanas.
    * Processa a imagem usando Redes Neurais (YOLOv8) para identificar e contar veículos.
    * Executa a lógica adaptativa e envia comandos de estado para o hardware.
    * Renderiza a interface Web de controle (Streamlit).

### 2. Controlador de Hardware (Músculo - Arduino/C++)
* **Linguagem:** C++ (Wiring)
* **Função:**
    * Recebe os comandos do servidor Python.
    * Controla os relés e LEDs físicos com precisão de tempo real (sem uso de delays bloqueantes).

## Tech Stack

**High-Level (Visão, Lógica e Web)**
* Python 3
* OpenCV & YOLOv8 (Visão Computacional)
* Streamlit (Interface Web)
* Pandas & Matplotlib (Data Science e BI)
* PySerial (Comunicação)

**Low-Level (Hardware)**
* C++ / Arduino IDE

## Instalação e Configuração

### 1. Configurando o Ambiente Python (Servidor)

Abra o terminal na pasta raiz do projeto e crie o ambiente virtual:

````bash 
python -m venv .venv
Ative o ambiente virtual:

No Windows:

PowerShell
.venv\Scripts\activate

No Linux/Mac:
Bash
source .venv/bin/activate
Instale todas as dependências do projeto:

Bash
pip install opencv-python ultralytics streamlit pandas matplotlib pyserial
````
2. Configurando o Hardware (Arduino)
Abra a Arduino IDE.

Carregue o arquivo traffic_control.ino (localizado na pasta do firmware).

Conecte o Arduino via cabo USB e faça o upload para a placa.

Verifique a porta COM (ex: COM3) e atualize no script Python, se necessário.

* Como Executar o Sistema
Com o ambiente virtual ativado e o Arduino conectado, inicie o servidor rodando:

Bash
streamlit run dashboard.py
O painel do CCO abrirá automaticamente no seu navegador.

* Roadmap e Histórico de Desenvolvimento
[x] Sprint 1: Prova de Conceito (PoC) da Visão Computacional (YOLOv8) e Mapeamento de Zonas Espaciais.

[x] Sprint 2: Máquina de Estados e Firmware C++ (Controle de LEDs físico).

[x] Sprint 3: Integração Serial (Python e C++) e Módulo de Log de Dados.

[x] Sprint 4: Engenharia de Resiliência (Fail-Safe/Watchdog no hardware) e Prioridade de Emergência na IA.

[x] Sprint 5: Matemática Adaptativa (Thresholds) para fim do "Efeito Ping-Pong".

[x] Sprint 6: Desenvolvimento do Dashboard Web (Streamlit) com Modo Override.

[x] Sprint 7: Integração de Business Intelligence (Gráficos Pandas/Matplotlib) na interface.

[ ] Sprint 8: Montagem do protótipo e da maquete física do cruzamento.

* Licença

Este projeto é parte do Trabalho de Conclusão de Curso (TCC) em Engenharia de Software.
