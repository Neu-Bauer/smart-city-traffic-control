#  Smart City Traffic Control (Hybrid IoT System)

> **Status:** - Em Desenvolvimento (Fase de Arquitetura e Integração)

Um sistema de gestão de tráfego inteligente que une a facilidade do **Python** para Inteligência Artificial com a performance do **C++** para controle de hardware. O projeto utiliza câmeras para analisar o fluxo de veículos e controlar semáforos físicos em tempo real.

---

## - Arquitetura da Solução

O sistema opera em uma arquitetura Mestre-Escravo via comunicação Serial:

### 1. Raspberry Pi / PC
* **Linguagem:** **Python 3**.
* **Bibliotecas:** `OpenCV`, `YOLOv8` (IA), `PySerial`.
* **Função:**
    * Captura imagens das câmeras urbanas.
    * Processa a imagem usando Redes Neurais para contar veículos.
    * Toma a decisão lógica (ex: "Trânsito pesado na Via A, abrir semáforo").
    * Envia o comando via USB/Serial para o controlador.

### 2. Arduino / ESP32
* **Linguagem:** **C++** (Wiring).
* **Função:**
    * Recebe os comandos codificados do Python (ex: string JSON ou bytes).
    * Controla as portas digitais (Relés/LEDs) com precisão de tempo real.
    * Garante a segurança do ciclo semafórico (não deixar dois sinais verdes ao mesmo tempo).

---

## - Tech Stack

### High-Level (Visão & Lógica)
* ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) **Python:** Script principal de automação.
* ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white) **OpenCV / YOLO:** Processamento de imagem e detecção de objetos.

### Low-Level (Hardware)
* ![C++](https://img.shields.io/badge/C++-00599C?style=flat&logo=c%2B%2B&logoColor=white) **C++:** Firmware do microcontrolador.
* ![Arduino](https://img.shields.io/badge/Arduino-00979D?style=flat&logo=arduino&logoColor=white) **Arduino IDE:** Ambiente de desenvolvimento embarcado.

---

## - Roadmap

- [x] Definição da Arquitetura Híbrida (Python + C++).
- [ ] Script Python: Leitura de câmera e detecção básica.
- [ ] Firmware C++: Controle dos LEDs e máquina de estados do semáforo.
- [ ] Integração: Criar protocolo de comunicação Serial (Python conversa com C++).
- [ ] Montagem da maquete física.

---

## - Licença

Este projeto é parte do Trabalho de Conclusão de Curso (TCC) em Engenharia de Software.
