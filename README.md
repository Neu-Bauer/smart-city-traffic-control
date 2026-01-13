#  Smart City Traffic Control

> **Status:** - Em Desenvolvimento (Fase de Arquitetura e Prototipagem)

Um sistema inteligente de gestão de tráfego urbano que utiliza **Visão Computacional** para analisar o fluxo de veículos em tempo real e ajustar dinamicamente os temporizadores dos semáforos, substituindo os modelos estáticos tradicionais.

---

## - Arquitetura da Solução (Planejada)

O projeto é dividido em microsserviços containerizados para garantir escalabilidade e facilidade de deploy.

### 1. Vision Service 
* **Tecnologia:** Python, OpenCV, YOLOv8.
* **Função:** Captura o feed de vídeo das câmeras urbanas, detecta veículos e calcula a densidade da via. Envia esses dados (metadados) para a API.

### 2. Traffic Controller API  
* **Tecnologia:** Node.js, Express.
* **Função:** Recebe os dados de densidade, processa a lógica de decisão e define se o semáforo deve abrir ou fechar, priorizando vias congestionadas (Ambulâncias/Emergência no futuro).

### 3. Infraestrutura 
* **Docker:** Orquestração dos serviços.
* **Database:** Armazenamento histórico de fluxo para gerar relatórios de mobilidade.

---

## - Tech Stack

* **Linguagens:** Python (IA/Vision), JavaScript/Node.js (Backend).
* **Containerização:** Docker & Docker Compose.
* **Computer Vision:** YOLO (You Only Look Once) / OpenCV.

---

## - Roadmap

- [x] Definição da Arquitetura e Stack.
- [ ] Implementação do serviço de detecção de veículos (Python).
- [ ] Criação da API de controle de tráfego (Node.js).
- [ ] Configuração do ambiente Docker.
- [ ] Integração com maquete física (Simulação).

---

## - Licença

Este projeto é parte do Trabalho de Conclusão de Curso (TCC) em Engenharia de Software.
