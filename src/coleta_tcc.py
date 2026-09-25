"""
coleta_tcc.py — Coleta acadêmica padronizada do Sistema AirPrice.

Executa, sem interface gráfica, todas as rotas cadastradas em
`ROTAS_DISPONIVEIS` para as janelas de antecedência do estudo
(7, 15, 30 e 90 dias), sempre em modo headless e com registro de
linhas vazias quando uma rota não retorna preço (`registrar_sem_dados`).

O objetivo não é encontrar a melhor data de compra, e sim registrar o
preço observado para cada combinação de rota e antecedência.

Uso:
    python src/coleta_tcc.py
"""

import sys
from datetime import datetime, timedelta

from scraper_passagens import (
    ROTAS_DISPONIVEIS,
    executar_rotas_sequencial,
    stop_event,
)


class ConsoleController:
    """Substitui a GUI por saída de texto no terminal (mesma interface de log usada pela GUI)."""

    def log(self, msg, _tipo="info"):
        print(msg)

    def log_ok(self, msg):
        print(f"[OK] {msg}")

    def log_err(self, msg):
        print(f"[ERRO] {msg}")

    def log_warn(self, msg):
        print(f"[WARN] {msg}")

    def log_info(self, msg):
        print(f"[INFO] {msg}")

    def info(self, title, msg):
        print(f"{title}: {msg}")

    def warn(self, title, msg):
        print(f"{title}: {msg}")

    def error(self, title, msg):
        print(f"{title}: {msg}")

def main():
    """Executa todas as rotas para as janelas [7, 15, 30, 90] dias e imprime o resumo final."""
    rotas = list(ROTAS_DISPONIVEIS.keys())
    janelas = [7, 15, 30, 90]
    
    stop_event.clear()
    controller = ConsoleController()
    
    controller.log_info("Iniciando extracão de 4 rotas e 4 janelas de antecedência.")
    
    total_resultados = []
    
    for janela in janelas:
        data_voo = (datetime.now() + timedelta(days=janela)).strftime("%Y-%m-%d")
        controller.log_info(f"\n==============================================")
        controller.log_info(f"Pesquisando antecedência de {janela} dias (Voo: {data_voo})")
        controller.log_info(f"==============================================")
        
        base_config = {
            "data_voo_str": data_voo,
            "user_agent_label": "Chrome Desktop (padrao)",
            "modo_privacidade": "Sem cookies (perfil limpo)",
            "experimento_id": f"EXTRACAO_{janela}D",
            "repeticoes": 1,
            "headless": True,
            "show_dialogs": False,
            "registrar_sem_dados": True,
        }
        
        resultados = executar_rotas_sequencial(
            controller,
            rotas,
            ["LATAM"],
            base_config,
        )
        total_resultados.extend(resultados)
        controller.log_ok(f"Coleta da janela de {janela} dias finalizada com {len(resultados)} registro(s).")
    
    controller.log_ok(f"\nEXTRAÇÃO COMPLETA! Total de {len(total_resultados)} registros coletados no total.")

if __name__ == "__main__":
    main()
