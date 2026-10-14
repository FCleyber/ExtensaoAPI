import argparse
import json
from pathlib import Path

import requests

SERIE_IPCA = 433
DESCRICAO = "IPCA - variação mensal (%)"
BASE_URL = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{SERIE_IPCA}/dados"


def coletar_ipca(inicio: str | None, fim: str | None, timeout: int = 20) -> list[dict]:
    """Busca a série do IPCA no SGS. Datas no formato dd/mm/aaaa."""
    params = {"formato": "json"}
    if inicio:
        params["dataInicial"] = inicio
    if fim:
        params["dataFinal"] = fim

    resp = requests.get(BASE_URL, params=params, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def main():
    parser = argparse.ArgumentParser(description="Coleta o IPCA (SGS 433) do BACEN")
    parser.add_argument("--inicio", default=None, help="dd/mm/aaaa")
    parser.add_argument("--fim", default=None, help="dd/mm/aaaa")
    parser.add_argument("--saida", default="dados_ipca.json", help="Arquivo de saída (JSON)")
    args = parser.parse_args()

    print(f"Coletando IPCA (SGS {SERIE_IPCA}) — {DESCRICAO}...")
    try:
        dados = coletar_ipca(args.inicio, args.fim)
    except requests.RequestException as e:
        print(f"Erro ao coletar: {e}")
        raise SystemExit(1)

    print(f"  -> {len(dados)} observações")

    saida_path = Path(args.saida)
    saida_path.write_text(
        json.dumps(
            {"codigo_sgs": SERIE_IPCA, "descricao": DESCRICAO, "dados": dados},
            ensure_ascii=False, indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Salvo em {saida_path.resolve()}")


if __name__ == "__main__":
    main()