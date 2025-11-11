#  Dispositivo Vestível com Feedback Háptico para Auxílio à Mobilidade

> **Este projeto desenvolve um protótipo de dispositivo vestível (bracelete háptico) de baixo custo para auxiliar a mobilidade de pessoas com deficiência visual, utilizando feedback vibrotátil discreto e ergonômico.**

---

## Sobre o Projeto

As tecnologias assistivas para mobilidade de pessoas cegas frequentemente apresentam limitações como alto custo, baixa ergonomia ou dependência do canal auditivo (que compromete a percepção espacial).

Nossa solução propõe um sistema modular, regido por uma arquitetura Cliente-Servidor robusta, que utiliza **seis atuadores de vibração** com um **espaçamento otimizado de 2,5 cm** para melhorar a acuidade espacial e a distinção precisa dos padrões hápticos.

A principal contribuição é a **lógica de padrões híbrida**, que associa estímulos vibrotáteis dinâmicos a obstáculos em movimento e estímulos estáticos a objetos imóveis, enriquecendo a informação tátil transmitida.

---

## Hardware do Dispositivo

| Componente | Detalhe | Função |
| :--- | :--- | :--- |
| **Bracelete** | Impresso em 3D. | Plataforma vestível que hospeda os atuadores. |
| **Atuadores** | **6 Motores de vibração**. | Fornecer o feedback vibrotátil. |
| **Módulo de Controle** | PCI com **8 Canais independentes**. | Acionar e controlar a intensidade dos motores. |
| **Microcontrolador** | **Arduino Uno** (ou similar, como um ESP32 para versão final). | Servidor (Back-End) para executar o firmware e gerenciar o acionamento via PWM. |
| **Otimização** | Espaçamento de **2,5 cm** entre os atuadores. | Reduzir a confusão de estímulos e melhorar a acuidade tátil espacial. |
---

## Software e Arquitetura do Sistema

O sistema é dividido em duas camadas principais, comunicando-se via Serial Assíncrona.

### 1. Servidor (Firmware)

-   **Tecnologia:** C++ (para Arduino).
-   **Função:** Recebe comandos serializados e os traduz em sinais **PWM (Pulse Width Modulation)** para controlar a intensidade e a duração da vibração de cada um dos seis motores.

### 2. Cliente (Interface Gráfica)

-   **Tecnologia:** Python 3 + Tkinter.
-   **Função:** Interface Gráfica do Usuário (GUI) para:
    * Conexão/Desconexão Serial.
    * Seleção e envio de padrões vibrotáteis pré-definidos (ex: "Movimento Direita", "Perigo").
    * Criação de novas sequências de padrões (prototipagem).

### Exemplo de Padrões Hápticos

| Padrão | Tipo | Princípio Tátil | Objetivo Semântico |
| :--- | :--- | :--- | :--- |
| **Movimento Direita** | Dinâmico | Ativação sequencial (Movimento Aparente Tátil). | Sinalizar obstáculo dinâmico se deslocando no campo de visão. |
| **Estático Direita** | Estático | Codificação espacial (Ativação constante). | Sinalizar obstáculo imóvel (parede, poste) no lado direito. |

---

## Como Executar o Projeto (Getting Started)

Siga estas instruções para configurar e testar o projeto.

### Pré-requisitos

1.  **Hardware:** Um Arduino Uno ou equivalente.
2.  **Software:**
    * IDE do Arduino (para fazer o upload do firmware).
    * Python 3.
    * A biblioteca `pyserial` do Python:
        ```bash
        pip install pyserial
        ```

### Instalação e Configuração

1.  **Clonar o Repositório:**
    ```bash
    git clone [https://github.com/Assistive-Robotics/haptic-controller/tree/main/vibracao/c%C3%B3digo%20padr%C3%B5es%20de%20vibra%C3%A7%C3%A3o%20-%20vers%C3%A3o%20Artigo]
    cd haptic-controller
    ```

2.  **Firmware (Servidor):**
    * Abra o arquivo na IDE do Arduino.
    * Conecte o Arduino Uno ao seu computador.
    * Faça o upload do código para a placa.

3.  **Interface (Cliente):**
    * Execute o script Python da interface gráfica, garantindo que a porta serial do seu Arduino esteja configurada corretamente (por exemplo, `COM3` no Windows ou `/dev/ttyACM0` no Linux).
    ```bash
    ```

### Uso

Após a execução, utilize a GUI para selecionar os padrões vibrotáteis e enviá-los ao Arduino, observando o comportamento dos atuadores conectados ao bracelete.

---

## Trabalhos Futuros (Roadmap)

O projeto está em constante evolução. As próximas etapas incluem:

-   [ ] **Integração com Visão Computacional:** Conexão com câmeras/sensores de profundidade (RGB-D) para detecção de obstáculos em tempo real.
-   [ ] **Estudos de Usabilidade:** Realização de ensaios com pessoas com deficiência visual para validar a eficácia e usabilidade dos padrões.
-   [ ] **Miniaturização:** Substituição do Arduino Uno por um microcontrolador menor (ex: ESP32) e otimização da PCI.
-   [ ] **Fonte de Energia:** Inclusão de bateria recarregável para portabilidade total.

---
