import os
from enum import Enum
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. SETUP DA API
load_dotenv()
client = genai.Client()
MODELO_BASE = 'gemini-2.5-flash'

# 2. VARIÁVEIS DE ESTADO E ENTIDADES
class Estado(Enum):
    JOGANDO = "Jogando"
    GAME_OVER = "Game Over"
    VITORIA = "Vitória"

class Jogador:
    def __init__(self):
        self.estado_atual = Estado.JOGANDO
        self.hp = 10
        self.inventario = ["isqueiro", "pe de cabra"]

class Inimigo:
    def __init__(self):
        self.nome = "Homem Pálido"
        self.hp = 12
        self.alerta = False # Define se o monstro notou o jogador

# 3. ESTRUTURAÇÃO DO TURNO (Motor de Resolução)
class RespostaTurno(BaseModel):
    narrativa: str
    dica_sistema: str # Usado para dar feedback mecânico ou de sobrevivência
    alteracao_hp_jogador: int
    alteracao_hp_inimigo: int
    inimigo_notou_jogador: bool
    item_recebido: Optional[str]
    item_removido: Optional[str]

# 4. CONFIGURAÇÕES DE REGRAS E BALANCEAMENTO
SYSTEM_PROMPT = """Você é o Motor Lógico e Narrador de um RPG de texto de 'Caçador: A Revanche'. 
O tom é desesperador, mas o jogo deve ser JUSTO e estruturado.

REGRAS OBRIGATÓRIAS DE GAMEPLAY:
1. AÇÕES DE BUSCA/INSPEÇÃO: Se o jogador 'inspecionar' ou agir com cautela, NÃO cause dano imediato. Descreva os pontos fracos ou o nível de ameaça. O monstro só ataca se o jogador fizer barulho ou for hostil primeiro.
2. COMBATE: Se o jogador atacar com o 'pé de cabra', ele causa dano real (reduza o hp_inimigo entre -3 e -5). O monstro revida causando dano ao jogador (entre -1 e -3).
3. FEEDBACK MECÂNICO: Preencha o campo 'dica_sistema' com instruções úteis (ex: "O monstro está quase morto", "A pele dele resiste a socos", "Ele não te viu ainda. É possível fugir").
4. ESTADO DE ALERTA: Use o boolean 'inimigo_notou_jogador' para informar ao sistema se o furtividade acabou.
"""

FILTROS_SEGURANCA = [
    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=types.HarmBlockThreshold.BLOCK_NONE),
    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
]

# 5. FUNÇÃO DE PROCESSAMENTO
def processar_turno(input_jogador: str, jogador: Jogador, inimigo: Inimigo, ambiente: str) -> RespostaTurno:
    status_alerta = "O monstro JÁ NOTOU o jogador e está agressivo." if inimigo.alerta else "O monstro está distraído comendo e NÃO notou o jogador ainda."
    
    prompt = f"""
    Cenário: {ambiente}
    Jogador: HP {jogador.hp}, Inventário: {jogador.inventario}
    Inimigo: {inimigo.nome} (HP: {inimigo.hp}). {status_alerta}
    
    Ação do Jogador: "{input_jogador}"
    
    Gere a narrativa da consequência e defina as alterações matemáticas.
    """
    
    try:
        resposta = client.models.generate_content(
            model=MODELO_BASE,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=RespostaTurno,
                temperature=0.5, # Reduzido levemente para garantir coerência no combate
                safety_settings=FILTROS_SEGURANCA
            )
        )
        if not resposta.text:
            raise ValueError("Resposta vazia da IA.")
        return RespostaTurno.model_validate_json(resposta.text)
        
    except Exception as e:
        print(f"\n[DEBUG - ERRO]: {e}")
        return RespostaTurno(
            narrativa="Erro de conexão. O mundo congela por um segundo.",
            dica_sistema="Tente digitar sua ação novamente.",
            alteracao_hp_jogador=0, alteracao_hp_inimigo=0, inimigo_notou_jogador=inimigo.alerta,
            item_recebido=None, item_removido=None
        )

# 6. O LOOP PRINCIPAL
def main():
    jogador = Jogador()
    inimigo = Inimigo()
    ambiente_atual = "Você é um(a) caçador(a). Boatos de uma criatura horrível correm pela cidade. Sua busca pela criatura te levou até um beco escuro cheirando a urina e lixo. Há garrafas quebradas no chão."
    
    print("=== CAÇADOR: A REVANCHE - O DESPERTAR ===\n")
    print(ambiente_atual)
    print(f"Um {inimigo.nome} está de costas para você, devorando um cachorro de rua. O som de ossos quebrando ecoa.\n")
    
    while jogador.estado_atual == Estado.JOGANDO:
        comando = input("> ")
        if comando.lower() in ['sair', 'quit']: break
            
        print("...")
        
        resultado = processar_turno(comando, jogador, inimigo, ambiente_atual)
        
        # Aplicação das regras do Árbitro
        jogador.hp += resultado.alteracao_hp_jogador
        inimigo.hp += resultado.alteracao_hp_inimigo
        inimigo.alerta = resultado.inimigo_notou_jogador
        
        if resultado.item_recebido and resultado.item_recebido not in jogador.inventario:
            jogador.inventario.append(resultado.item_recebido.lower())
        if resultado.item_removido and resultado.item_removido.lower() in jogador.inventario:
            jogador.inventario.remove(resultado.item_removido.lower())
            
        ambiente_atual += f" Ultima ação: {resultado.narrativa}"
        
        # Resoluções de morte
        if inimigo.hp <= 0:
            resultado.narrativa += f"\n\nO {inimigo.nome} desaba no chão imundo, sem vida."
            resultado.dica_sistema = "Ameaça eliminada. Você sobreviveu à noite."
            jogador.estado_atual = Estado.VITORIA
        elif jogador.hp <= 0:
            resultado.narrativa += "\n\nVocê sucumbiu à escuridão. Fim de Jogo."
            jogador.estado_atual = Estado.GAME_OVER

        # Exibição estruturada para o jogador
        print(f"\n{resultado.narrativa}")
        print(f"\n[SISTEMA]: {resultado.dica_sistema}")
        
        print("-" * 50)
        status_inimigo = "Morto" if inimigo.hp <= 0 else "Alerta" if inimigo.alerta else "Distraído"
        print(f"CAÇADOR [HP: {jogador.hp}/10 | Inventário: {jogador.inventario}]")
        if inimigo.hp > 0:
            # Não exibe o HP exato do monstro para manter o mistério, mas dá uma ideia
            saude_monstro = "Inteiro" if inimigo.hp > 8 else ("Ferido" if inimigo.hp > 4 else "Gravemente Ferido")
            print(f"ALVO    [{inimigo.nome} | Estado: {status_inimigo} | Saúde: {saude_monstro}]")
        print("-" * 50 + "\n")

if __name__ == "__main__":
    main()