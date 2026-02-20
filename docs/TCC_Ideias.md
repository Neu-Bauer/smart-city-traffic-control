    Dia 01 (05/02/26) 

- Prova de Conceito (PoC) da Visão Computacional

- Inicialização do projeto e configuração do ambiente virtual (.venv).

- Testes preliminares com o modelo YOLOv8 (yolov8n.pt) em vídeos de trânsito para validar a capacidade da IA de reconhecer e classificar diferentes tipos de veículos (carros, motos, ônibus, caminhões).

    Dia 02 (07/02/26) 

- Mapeamento Espacial e Contagem

- Definição da geometria da via utilizando o OpenCV.

- Criação dos polígonos de detecção (Zonas Amarela e Magenta) para limitar o campo de visão da IA apenas às faixas de interesse, filtrando ruídos do cenário.

- Implementação da lógica de contagem de veículos por área.

    Dia 03 (10/02/26)  
    
- A Máquina de Estados (Cérebro v1)

- Desenvolvimento da primeira versão do traffic_controller.py.

- Estruturação da máquina de estados do semáforo (Verde -> Amarelo -> Vermelho de Segurança -> Verde).

- Criação da lógica de decisão inicial, baseada na comparação simples do volume das filas.

    Dia 04 (12/02/26) 
    
- O Hardware (Músculo do Sistema)

- Criação do diretório isolado firmware-cpp para o código de baixo nível.

- Escrita do firmware do microcontrolador (Arduino) em C++ (traffic_control.ino), mapeando as portas digitais para os módulos de relé/LEDs.

- Validação do circuito elétrico e da lógica de acendimento através do simulador Wokwi.

    Dia 05 (14/02/26)  
    
- Integração Serial e Coleta de Dados

- Desenvolvimento do módulo traffic_comm.py para estabelecer a ponte de comunicação serial entre o servidor Python e o Arduino.

- Criação do traffic_logger.py, garantindo que toda troca de estado seja registrada em um arquivo .csv para futura geração de gráficos e análise de eficiência para o TCC.

    Dia 06 (16/02/26) 
    
- Prioridade Absoluta (Módulo de Emergência)

- Evolução da lógica de visão computacional para rastreamento de veículos prioritários (usando classes de veículos pesados como proxy no protótipo).

- Implementação da "Regra de Ouro": interrupção da contagem normal e injeção do valor de override (Fila = 999) para forçar a abertura imediata do semáforo, simulando a passagem de ambulâncias.

    Dia 07 (18/02/26) 

- Matemática Adaptativa e Otimização de Tráfego

- Refatoração completa do traffic_controller.py para eliminar o "efeito ping-pong".

- Implementação de Limiares de Ação (Thresholds): fila mínima para justificar a troca e fila máxima para forçar o escoamento de engarrafamentos.

- Adição do temporizador de limite de espera (resolvendo o "problema da madrugada" para veículos isolados).

    Dia 08 (19/02/26)  
    
- Engenharia de Resiliência (Fail-Safe)

- Implementação de tolerância a falhas no firmware C++ do Arduino.

- Criação do sistema "Watchdog" (Cão de Guarda) usando a função millis() no lugar de delay().

- Garantia de Degradação Graciosa: se a conexão com o servidor Python for perdida, o hardware entra automaticamente em um modo autônomo e temporizado de segurança.

    Dia 09 (20/02/26)  
    
- Centro de Controle Operacional (Interface Web)

- Migração do terminal em texto para um Dashboard interativo profissional utilizando o Streamlit (dashboard.py).

- Otimização extrema de performance de vídeo (Frame Skipping, redimensionamento visual e redução da resolução de inferência da IA para imgsz=320).

- Implementação da Sobrescrita Manual (Botão de "Modo Noturno" / Amarelo Intermitente), permitindo intervenção humana no sistema automatizado.

    Dia 10 (20/02/26) 
    
- BI Integrado e Tratamento de Dados Estatísticos

- Desenvolvimento inicial do módulo de Ciência de Dados com pandas e matplotlib para extração de métricas de eficiência.

- Correção e sanitização da base de dados (conversão de strings temporais como "10.72s" para floats numéricos), permitindo o cálculo da média do tempo dinâmico de sinal verde.

- Tratamento de outliers na visualização de dados (remoção de picos de fila valor 999 gerados pelo modo de emergência) para evitar distorção na escala do Gráfico de Volume de Filas.

- Substituição do eixo X temporal por um indexador de intervenções, resolvendo problemas de sobreposição de texto nos relatórios.

- Automação de BI (Business Intelligence): Refatoração da interface web (dashboard.py) com um sistema de Abas (Tabs), embutindo a renderização dos relatórios visuais estáticos de forma dinâmica na própria tela do Centro de Controle Operacional.

- Status Atual: Arquitetura de software (Visão, Controle, Comunicação e Interface Web com BI) completamente validada e finalizada. O próximo passo será focado exclusivamente no hardware físico (maquete, LEDs, resistores e posicionamento de câmera).