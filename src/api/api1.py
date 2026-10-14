"""API 1: IPCA mensal (série 433 do SGS/Banco Central) devolvido em JSON.

Usa apenas a biblioteca padrão do Python 3.8+; não há nada para instalar.

Rodar:   python api1.py
Abrir:   http://127.0.0.1:8000/ipca
"""
import json
import os
import re
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

SERIE = 433
URL_BCB = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.%d/dados?formato=json" % SERIE
FONTE = (
    "IPCA, produzido pelo IBGE e disponibilizado pelo Banco Central do Brasil "
    "(SGS, série %d)" % SERIE
)
UNIDADE = "variação percentual mensal"
PADRAO_MES = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
CACHE_SEGUNDOS = 3600

_cache = {"quando": 0.0, "dados": None}


def baixar_serie():
    """Baixa a série completa no SGS e devolve a lista JSON bruta."""
    req = urllib.request.Request(URL_BCB, headers={"User-Agent": "ExtensaoAPI/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def normalizar(registros):
    """Converte [{"data": "01/08/2026", "valor": "-0.32"}] em
    [{"mes": "2026-08", "ipca_mensal_pct": -0.32}], em ordem cronológica."""
    saida = []
    for r in registros:
        _dia, mes, ano = r["data"].split("/")
        saida.append({"mes": "%s-%s" % (ano, mes), "ipca_mensal_pct": float(r["valor"])})
    saida.sort(key=lambda x: x["mes"])
    return saida


def filtrar(dados, inicio=None, fim=None):
    """Mantém só os meses entre inicio e fim (AAAA-MM, inclusive)."""
    return [
        d for d in dados
        if (inicio is None or d["mes"] >= inicio) and (fim is None or d["mes"] <= fim)
    ]


def obter_dados():
    """Série normalizada, com cache em memória de 1 hora."""
    agora = time.time()
    if _cache["dados"] is None or agora - _cache["quando"] > CACHE_SEGUNDOS:
        _cache["dados"] = normalizar(baixar_serie())
        _cache["quando"] = agora
    return _cache["dados"]


def montar_resposta(inicio=None, fim=None):
    """Monta o corpo da resposta de /ipca. Levanta ValueError se os parâmetros forem inválidos."""
    for nome, valor in (("inicio", inicio), ("fim", fim)):
        if valor is not None and not PADRAO_MES.match(valor):
            raise ValueError("Parâmetro '%s' inválido: use o formato AAAA-MM (ex.: 2026-01)." % nome)
    if inicio and fim and inicio > fim:
        raise ValueError("'inicio' não pode ser posterior a 'fim'.")
    todos = obter_dados()
    selecionados = filtrar(todos, inicio, fim)
    return {
        "fonte": FONTE,
        "serie_sgs": SERIE,
        "unidade": UNIDADE,
        "ultimo_mes_disponivel": todos[-1]["mes"] if todos else None,
        "total": len(selecionados),
        "dados": selecionados,
    }


AJUDA = {
    "api": "API 1 - IPCA mensal em JSON",
    "fonte": FONTE,
    "rotas": {
        "GET /": "esta ajuda",
        "GET /ipca": "série completa (desde 1980-01)",
        "GET /ipca?inicio=AAAA-MM&fim=AAAA-MM": "intervalo de meses, inclusive; os dois parâmetros são opcionais",
    },
    "exemplo": "/ipca?inicio=2026-01&fim=2026-08",
}


class Handler(BaseHTTPRequestHandler):
    def _json(self, status, corpo):
        dados = json.dumps(corpo, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/":
            return self._json(200, AJUDA)
        if url.path == "/ipca":
            params = parse_qs(url.query)
            try:
                corpo = montar_resposta(
                    params.get("inicio", [None])[0], params.get("fim", [None])[0]
                )
            except ValueError as erro:
                return self._json(400, {"erro": str(erro)})
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
                return self._json(502, {"erro": "Não foi possível consultar o SGS do Banco Central agora. Tente novamente."})
            return self._json(200, corpo)
        return self._json(404, {"erro": "Rota não encontrada. Veja GET /"})

    def log_message(self, formato, *args):
        print("%s %s" % (self.address_string(), formato % args))


def main():
    host = os.environ.get("HOST", "127.0.0.1")
    porta = int(os.environ.get("PORT", "8000"))
    servidor = ThreadingHTTPServer((host, porta), Handler)
    print("API 1 no ar: http://%s:%d/ipca  (Ctrl+C para parar)" % (host, porta))
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrado.")


if __name__ == "__main__":
    main()
