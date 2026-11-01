"""API 2 e página de uso: compara o reajuste de um produto com o IPCA acumulado.

Roda junto com a API 1 (rota /ipca). Só biblioteca padrão do Python 3.8+.

Rodar:   python src/api/api2.py
Abrir:   http://127.0.0.1:8000/

Rotas:
  GET /          página de uso (formulário)
  GET /comparar  API 2: ?preco_inicial=&mes_inicial=&preco_final=&mes_final=
  GET /ipca      API 1: série do IPCA
  GET /ajuda     lista de rotas em JSON

Todo o cálculo é feito aqui, em código. O LLM, se estiver ativado, só reescreve
a frase final (ver src/llm/llm_cliente.py); nunca calcula.
"""
import json
import math
import os
import sys
import urllib.error
from http.server import ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import api1

LLM_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "llm")
LIMIAR_PROXIMO_PP = 1.0  # diferença de até 1 ponto percentual = "próximo"
AVISO = "Resultado informativo; não substitui orientação econômica ou profissional."


class ErroEntrada(ValueError):
    """Entrada inválida do usuário (vira HTTP 400)."""


def _numero(texto, nome):
    if texto is None or not texto.strip():
        raise ErroEntrada("Informe '%s'." % nome)
    try:
        valor = float(texto.strip().replace(",", "."))
    except ValueError:
        raise ErroEntrada("'%s' deve ser um número (ex.: 10,80)." % nome)
    if not math.isfinite(valor) or valor <= 0:
        raise ErroEntrada("'%s' deve ser um número maior que zero." % nome)
    return valor


def _mes(texto, nome):
    if texto is None or not api1.PADRAO_MES.match(texto.strip()):
        raise ErroEntrada("'%s' deve estar no formato AAAA-MM (ex.: 2026-01)." % nome)
    return texto.strip()


def acumular_ipca(serie, mes_inicial, mes_final):
    """IPCA acumulado (%) do mês SEGUINTE a mes_inicial até mes_final, inclusive.

    O mês inicial não entra porque o preço inicial já incorpora a inflação dele.
    Devolve (acumulado em %, lista dos meses considerados)."""
    meses = [d for d in serie if mes_inicial < d["mes"] <= mes_final]
    fator = 1.0
    for d in meses:
        fator *= 1 + d["ipca_mensal_pct"] / 100
    return (fator - 1) * 100, [d["mes"] for d in meses]


def classificar(diferenca_pp):
    if abs(diferenca_pp) <= LIMIAR_PROXIMO_PP:
        return "proximo"
    return "acima" if diferenca_pp > 0 else "abaixo"


def _template(classificacao, diferenca_pp, variacao, ipca):
    """Explicação padrão, sem LLM. Mesma lógica de llm_cliente.template_determinístico."""
    dif = abs(round(diferenca_pp, 1))
    if classificacao == "acima":
        return ("O reajuste de %.1f%% ficou acima da inflação do período (%.1f%%), "
                "uma diferença de %s pontos percentuais." % (variacao, ipca, dif))
    if classificacao == "abaixo":
        return ("O reajuste de %.1f%% ficou abaixo da inflação do período (%.1f%%), "
                "uma diferença de %s pontos percentuais." % (variacao, ipca, dif))
    return ("O reajuste de %.1f%% ficou próximo da inflação do período (%.1f%%), "
            "com diferença de apenas %s ponto(s) percentual(is)." % (variacao, ipca, dif))


def explicar(classificacao, diferenca_pp, variacao, ipca, mes_inicial, mes_final):
    """Usa o módulo do LLM (que já cai no template se o LLM estiver desligado ou falhar).
    Se o módulo não puder ser importado, usa o template local."""
    try:
        if LLM_DIR not in sys.path:
            sys.path.append(LLM_DIR)
        from llm_cliente import explicar_reajuste
        return explicar_reajuste(variacao, ipca, classificacao, mes_inicial, mes_final)
    except Exception:
        return _template(classificacao, diferenca_pp, variacao, ipca)


def comparar(preco_inicial, mes_inicial, preco_final, mes_final, serie):
    """Regra de cálculo do plano de ação (Campo 3). Levanta ErroEntrada se inválido."""
    if mes_final <= mes_inicial:
        raise ErroEntrada("'mes_final' deve ser posterior a 'mes_inicial'.")
    primeiro, ultimo = serie[0]["mes"], serie[-1]["mes"]
    if mes_inicial < primeiro or mes_final > ultimo:
        raise ErroEntrada(
            "Os meses devem estar entre %s e %s (período com dados do IPCA)." % (primeiro, ultimo))
    variacao = round((preco_final / preco_inicial - 1) * 100, 2)
    ipca_bruto, meses = acumular_ipca(serie, mes_inicial, mes_final)
    ipca = round(ipca_bruto, 2)
    diferenca = round(variacao - ipca, 2)
    classificacao = classificar(diferenca)
    return {
        "entrada": {
            "preco_inicial": preco_inicial, "mes_inicial": mes_inicial,
            "preco_final": preco_final, "mes_final": mes_final,
        },
        "variacao_preco_pct": variacao,
        "ipca_acumulado_pct": ipca,
        "diferenca_pp": diferenca,
        "classificacao": classificacao,
        "meses_considerados": len(meses),
        "explicacao": explicar(classificacao, diferenca, variacao, ipca, mes_inicial, mes_final),
        "fonte": api1.FONTE,
        "aviso": AVISO,
    }


AJUDA = {
    "api": "API 2 - compara o reajuste de um produto com o IPCA acumulado",
    "fonte": api1.FONTE,
    "rotas": {
        "GET /": "página de uso (formulário)",
        "GET /comparar?preco_inicial=10&mes_inicial=2026-01&preco_final=10,80&mes_final=2026-08":
            "compara o reajuste com o IPCA acumulado do mês seguinte ao inicial até o final, inclusive",
        "GET /ipca": "API 1: série do IPCA (aceita inicio e fim, AAAA-MM)",
        "GET /ajuda": "esta ajuda",
    },
    "dica": "Qualquer rota aceita ?ref=nome para registrar quem acessou.",
}


PAGINA = r"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Seu reajuste acompanhou a inflação?</title>
<style>
  body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
         margin: 0; background: #f6f7f9; color: #1c1e21; }
  main { max-width: 34rem; margin: 0 auto; padding: 1.25rem; }
  h1 { font-size: 1.5rem; line-height: 1.25; }
  p.sub { color: #4b4f56; }
  form { background: #fff; border-radius: 12px; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,.12); }
  label { display: block; font-weight: 600; margin: .75rem 0 .25rem; }
  input { width: 100%; box-sizing: border-box; font-size: 1.1rem; padding: .6rem;
          border: 1px solid #c4c8ce; border-radius: 8px; }
  button { margin-top: 1rem; width: 100%; font-size: 1.1rem; padding: .75rem; border: 0;
           border-radius: 8px; background: #0b5ed7; color: #fff; font-weight: 600; cursor: pointer; }
  #r { margin-top: 1rem; }
  .card { background: #fff; border-radius: 12px; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,.12); }
  .frase { font-size: 1.15rem; font-weight: 600; }
  .erro { color: #a4161a; font-weight: 600; }
  ul { padding-left: 1.2rem; }
  small { color: #4b4f56; display: block; margin-top: .75rem; }
</style>
</head>
<body>
<main>
  <h1>Seu reajuste acompanhou a inflação?</h1>
  <p class="sub">Informe o preço de um produto em dois meses. Mostramos quanto ele subiu e quanto foi a inflação (IPCA) no mesmo período.</p>
  <form id="f">
    <label for="pi">Preço no mês inicial (R$)</label>
    <input id="pi" inputmode="decimal" placeholder="ex.: 10,00" required>
    <label for="mi">Mês inicial</label>
    <input id="mi" type="month" placeholder="AAAA-MM" required>
    <label for="pf">Preço no mês final (R$)</label>
    <input id="pf" inputmode="decimal" placeholder="ex.: 10,80" required>
    <label for="mf">Mês final</label>
    <input id="mf" type="month" placeholder="AAAA-MM" required>
    <button type="submit">Comparar</button>
  </form>
  <section id="r" aria-live="polite"></section>
  <small>Fonte: IPCA, produzido pelo IBGE e disponibilizado pelo Banco Central do Brasil (SGS, série 433). Resultado informativo; não substitui orientação econômica ou profissional.</small>
</main>
<script>
(function () {
  var ref = new URLSearchParams(location.search).get('ref');
  var r = document.getElementById('r');
  function v(id) { return document.getElementById(id).value; }
  function linha(texto) { var li = document.createElement('li'); li.textContent = texto; return li; }
  document.getElementById('f').addEventListener('submit', function (e) {
    e.preventDefault();
    var q = new URLSearchParams({
      preco_inicial: v('pi'), mes_inicial: v('mi'),
      preco_final: v('pf'), mes_final: v('mf')
    });
    if (ref) { q.set('ref', ref); }
    r.textContent = 'Calculando...';
    fetch('/comparar?' + q.toString())
      .then(function (resp) { return resp.json().then(function (d) { return { ok: resp.ok, d: d }; }); })
      .then(function (x) {
        r.textContent = '';
        var card = document.createElement('div');
        card.className = 'card';
        if (!x.ok) {
          card.className += ' erro';
          card.textContent = x.d.erro || 'Não foi possível calcular agora.';
        } else {
          var p = document.createElement('p');
          p.className = 'frase';
          p.textContent = x.d.explicacao;
          var ul = document.createElement('ul');
          ul.appendChild(linha('Variação do seu preço: ' + x.d.variacao_preco_pct + '%'));
          ul.appendChild(linha('Inflação (IPCA) no período: ' + x.d.ipca_acumulado_pct + '%'));
          ul.appendChild(linha('Diferença: ' + x.d.diferenca_pp + ' pontos percentuais'));
          card.appendChild(p);
          card.appendChild(ul);
        }
        r.appendChild(card);
      })
      .catch(function () {
        r.textContent = 'Não foi possível calcular agora. Tente novamente.';
      });
  });
})();
</script>
</body>
</html>
"""


class Handler(api1.Handler):
    def _html(self, corpo, ref, rota):
        dados = corpo.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        try:
            self.wfile.write(dados)
        finally:
            api1.registrar_acesso(ref, rota, 200)

    def _comparar(self, params, ref, rota):
        def p(nome):
            return params.get(nome, [None])[0]
        try:
            preco_inicial = _numero(p("preco_inicial"), "preco_inicial")
            preco_final = _numero(p("preco_final"), "preco_final")
            mes_inicial = _mes(p("mes_inicial"), "mes_inicial")
            mes_final = _mes(p("mes_final"), "mes_final")
            if mes_final <= mes_inicial:
                raise ErroEntrada("'mes_final' deve ser posterior a 'mes_inicial'.")
            serie = api1.obter_dados()
            resultado = comparar(preco_inicial, mes_inicial, preco_final, mes_final, serie)
        except ErroEntrada as erro:
            return self._json(400, {"erro": str(erro)}, ref, rota)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            return self._json(502, {"erro": "Não foi possível consultar o SGS do Banco Central agora. Tente novamente."}, ref, rota)
        except Exception:
            return self._json(500, {"erro": "Erro inesperado. Tente novamente."}, ref, rota)
        return self._json(200, resultado, ref, rota)

    def do_GET(self):
        url = urlparse(self.path)
        params = parse_qs(url.query)
        ref = params.get("ref", [None])[0]
        rota = url.path
        if rota == "/":
            return self._html(PAGINA, ref, rota)
        if rota == "/ajuda":
            return self._json(200, AJUDA, ref, rota)
        if rota == "/comparar":
            return self._comparar(params, ref, rota)
        return super().do_GET()  # /ipca (API 1) e 404


def main():
    # Na hospedagem (ex.: Render) a variável PORT existe: escuta em todas as interfaces.
    # Localmente, escuta só neste computador.
    host = os.environ.get("HOST") or ("0.0.0.0" if os.environ.get("PORT") else "127.0.0.1")
    porta = int(os.environ.get("PORT", "8000"))
    servidor = ThreadingHTTPServer((host, porta), Handler)
    print("App no ar (escutando em %s:%d). Abra http://127.0.0.1:%d/  (Ctrl+C para parar)" % (host, porta, porta))
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrado.")


if __name__ == "__main__":
    main()
