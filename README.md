# 🦇 Caçador: A Revanche - O Despertar (AI Text RPG)

Um motor de RPG de texto interativo baseado no universo de *Hunter: The Reckoning* (propriedade da Paradox Interactive). Este projeto utiliza a API do **Google Gemini (2.5 Flash)** para atuar como Mestre de Jogo (Narrador), combinando geração de história dinâmica via Inteligência Artificial com regras matemáticas determinísticas para cálculo de dano, inventário e sobrevivência.

## ✨ Funcionalidades

* **Narrativa Dinâmica:** Cada ação do jogador gera uma resposta única, interpretada e contextualizada pela IA.
* **Motor Híbrido:** A IA cria a história, mas o código Python local gerencia a mecânica real do jogo de forma determinística (HP do jogador, HP do monstro, inventário e status de alerta).
* **Saídas Estruturadas (Structured Outputs):** Utiliza a biblioteca `pydantic` para forçar o LLM a retornar um JSON estrito, garantindo consistência entre a narrativa e a matemática do sistema.

---

## 🛠️ Pré-requisitos

Antes de começar, você precisará ter o seguinte instalado em sua máquina:
* [Python 3.9 ou superior](https://www.python.org/downloads/)
* Git (para clonar o repositório)
* Uma chave de API gratuita do Google Gemini. Você pode gerar uma no [Google AI Studio](https://aistudio.google.com/).

---

## 🚀 Como baixar e jogar

Siga o passo a passo abaixo para configurar o ambiente e rodar o jogo no seu computador:

### 1. Clone o repositório
Abra o seu terminal (ou Prompt de Comando) e digite o comando abaixo para baixar o código:
```bash
git clone https://github.com/DreamchaserFF/rpg-texto-com-llm-python
cd rpg-texto-com-llm-python
```
*(Lembre-se de substituir o link acima pela URL real do seu repositório).*

### 2. Crie um Ambiente Virtual (Recomendado)
Para isolar as bibliotecas do jogo das instalações do seu sistema, crie e ative um ambiente virtual:

* **No Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
* **No Linux/Mac:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instale as dependências
Com o ambiente ativado, instale as bibliotecas necessárias para o jogo rodar:
```bash
pip install google-genai pydantic python-dotenv
```

### 4. Configure a sua Chave de API
Na pasta raiz do projeto (onde está o script do jogo), crie um arquivo chamado exatamente **`.env`**. Abra este arquivo em um editor de texto e adicione a sua chave do Gemini da seguinte forma:
```env
GEMINI_API_KEY=cole_sua_chave_aqui_sem_aspas
```

### 5. Inicie o Jogo
Com tudo configurado, basta rodar o script principal pelo terminal e tentar sobreviver à noite!
```bash
python main.py
```
*(Se o seu arquivo Python tiver outro nome, substitua `main.py` pelo nome correto).*

---

## 🎮 Como Jogar

* O jogo funciona através de comandos de texto. Leia a descrição do ambiente narrada pelo Sistema e digite a sua ação onde aparecer o símbolo `> `.
* Você tem liberdade total: pode tentar ser furtivo, procurar armas, inspecionar o cenário, fugir ou atacar.
* O inimigo reage de forma dinâmica às suas escolhas. Lembre-se: combates diretos e imprudentes costumam ser mortais. Use seu inventário e o cenário a seu favor.
* Preste atenção às dicas do `[SISTEMA]` geradas pelo Narrador para entender o desenrolar mecânico da cena.
* Para encerrar o jogo a qualquer momento, digite `sair` ou `quit`.

---

## ⚖️ Aviso Legal e Créditos

Este é um projeto estritamente educacional e sem fins lucrativos, desenvolvido como exercício de programação, lógica de estados e implementação de Inteligência Artificial (LLMs) em sistemas estruturados. 

*Caçador: A Revanche* (Hunter: The Reckoning), seus temas e conceitos relacionados são propriedade intelectual da **Paradox Interactive**. 
