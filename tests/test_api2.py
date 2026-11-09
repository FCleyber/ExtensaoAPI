"""Testes da API 2 (cálculo e comparação) e da página de uso.

Rodar (na raiz do repositório): python -m unittest discover -s tests -v

Os casos abaixo foram resolvidos à mão, antes do código. Usam uma série simulada
no formato do SGS, então não dependem da internet.

Caso principal (meses 2026-01 a 2026-03; o mês inicial não entra na conta):
  IPCA acumulado = (1,01 x 1,02) - 1 = 0,0302 = 3,02%
  100 -> 105: variação 5,00%, diferença +1,98 p.p.  -> acima
  100 -> 101: variação 1,00%, diferença -2,02 p.p.  -> abaixo
  100 -> 104: variação 4,00%, diferença +0,98 p.p.  -> próximo (até 1 p.p.)
"""
import csv
import json
import os
import sys
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "api"))
os.environ.pop("USAR_LLM_EXPLICACAO", None)  # os testes não chamam LLM

import api1
import api2

SERIE = api1.normalizar([
    {"data": "01/01/2026", "valor": "0.50"},
    {"data": "01/02/2026", "valor": "1.00"},
    {"data": "01/03/2026", "valor": "2.00"},
    {"data": "01/04/2026", "valor": "-0.32"},
])


def _get(url):
    try:
        with urllib.request.urlopen(url) as r:
            return r.status, r.headers.get("Content-Type", ""), r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type", ""), e.read().decode("utf-8")


class TestCalculo(unittest.TestCase):
    def test_ipca_acumulado_ignora_o_mes_inicial(self):
        acumulado, meses = api2.acumular_ipca(SERIE, "2026-01", "2026-03")
        self.assertAlmostEqual(acumulado, 3.02, places=6)
        self.assertEqual(meses, ["2026-02", "2026-03"])

    def test_acima(self):
        r = api2.comparar(100, "2026-01", 105, "2026-03", SERIE)
        self.assertEqual(r["variacao_preco_pct"], 5.00)
        self.assertEqual(r["ipca_acumulado_pct"], 3.02)
        self.assertEqual(r["diferenca_pp"], 1.98)
        self.assertEqual(r["classificacao"], "acima")
        self.assertEqual(r["meses_considerados"], 2)

    def test_abaixo(self):
        r = api2.comparar(100, "2026-01", 101, "2026-03", SERIE)
        self.assertEqual(r["diferenca_pp"], -2.02)
        self.assertEqual(r["classificacao"], "abaixo")

    def test_proximo(self):
        r = api2.comparar(100, "2026-01", 104, "2026-03", SERIE)
        self.assertEqual(r["diferenca_pp"], 0.98)
        self.assertEqual(r["classificacao"], "proximo")

    def test_exemplo_do_plano_de_acao(self):
        # R$ 10,00 -> R$ 10,80 (+8,0%) com IPCA acumulado de 5,0% -> acima, 3,0 p.p.
        serie = api1.normalizar([
            {"data": "01/01/2026", "valor": "0.00"},
            {"data": "01/02/2026", "valor": "5.00"},
        ])
        r = api2.comparar(10.00, "2026-01", 10.80, "2026-02", serie)
        self.assertEqual(r["variacao_preco_pct"], 8.0)
        self.assertEqual(r["ipca_acumulado_pct"], 5.0)
        self.assertEqual(r["diferenca_pp"], 3.0)
        self.assertEqual(r["classificacao"], "acima")

    def test_mes_com_ipca_negativo(self):
        # Só 2026-04 entra (-0,32%). 10,00 -> 9,90: -1,00%; diferença -0,68 -> próximo.
        r = api2.comparar(10.00, "2026-03", 9.90, "2026-04", SERIE)
        self.assertEqual(r["variacao_preco_pct"], -1.0)
        self.assertEqual(r["ipca_acumulado_pct"], -0.32)
        self.assertEqual(r["diferenca_pp"], -0.68)
        self.assertEqual(r["classificacao"], "proximo")

    def test_explicacao_cita_os_numeros_do_codigo(self):
        r = api2.comparar(100, "2026-01", 105, "2026-03", SERIE)
        self.assertIn("5,0%", r["explicacao"])
        self.assertIn("3,0%", r["explicacao"])
        self.assertIn("acima", r["explicacao"])

    def test_periodo_considerado_na_resposta(self):
        r = api2.comparar(100, "2026-01", 105, "2026-03", SERIE)
        self.assertEqual(r["periodo_considerado"], {"de": "2026-02", "ate": "2026-03"})
        self.assertEqual(r["ultimo_mes_disponivel"], "2026-04")

    def test_limite_de_5_anos(self):
        serie = api1.normalizar([{"data": "01/%02d/%d" % (m, a), "valor": "0.10"}
                                 for a in range(2019, 2027) for m in range(1, 13)])
        api2.comparar(10, "2020-01", 11, "2025-01", serie)  # exatamente 60 meses: aceito
        with self.assertRaises(api2.ErroEntrada):
            api2.comparar(10, "2020-01", 11, "2025-02", serie)  # 61 meses: recusado

    def test_mes_final_nao_posterior(self):
        with self.assertRaises(api2.ErroEntrada):
            api2.comparar(100, "2026-03", 105, "2026-03", SERIE)

    def test_mes_fora_da_serie(self):
        with self.assertRaises(api2.ErroEntrada):
            api2.comparar(100, "2025-12", 105, "2026-03", SERIE)
        with self.assertRaises(api2.ErroEntrada):
            api2.comparar(100, "2026-01", 105, "2026-05", SERIE)


class TestReserva(unittest.TestCase):
    """Plano B: se o Banco Central não responder, usa a cópia salva em dados/."""

    def setUp(self):
        self.original = (api1.baixar_serie, api1.RESERVA, dict(api1._cache))
        api1._cache.update({"quando": 0.0, "dados": None, "fonte": None})

        def falha():
            raise urllib.error.URLError("sem conexão (simulado)")
        api1.baixar_serie = falha

    def tearDown(self):
        api1.baixar_serie, api1.RESERVA, cache = self.original
        api1._cache.clear()
        api1._cache.update(cache)

    def test_usa_a_reserva_quando_o_banco_central_falha(self):
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        json.dump({"dados": [{"data": "01/01/2026", "valor": "0.50"},
                             {"data": "01/02/2026", "valor": "1.00"}]}, tmp)
        tmp.close()
        try:
            api1.RESERVA = tmp.name
            dados = api1.obter_dados()
            self.assertEqual(dados[-1], {"mes": "2026-02", "ipca_mensal_pct": 1.0})
            self.assertEqual(api1.fonte_dos_dados(), "reserva")
            r = api2.comparar(100, "2026-01", 101, "2026-02", dados)
            self.assertEqual(r["fonte_dados"], "reserva")
        finally:
            os.remove(tmp.name)

    def test_sem_reserva_o_erro_original_sobe(self):
        api1.RESERVA = "/caminho/que/nao/existe.json"
        with self.assertRaises(urllib.error.URLError):
            api1.obter_dados()

    def test_reserva_do_repositorio_e_valida(self):
        dados = api1.carregar_reserva()
        self.assertGreater(len(dados), 500)
        self.assertEqual(dados[0]["mes"], "1980-01")


class TestServidor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        api1._cache["dados"] = SERIE
        api1._cache["quando"] = 1e18
        cls.log = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
        cls.log.close()
        os.remove(cls.log.name)
        api1.LOG_ACESSOS = cls.log.name
        cls.srv = api2.ThreadingHTTPServer(("127.0.0.1", 0), api2.Handler)
        cls.base = "http://127.0.0.1:%d" % cls.srv.server_address[1]
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        if os.path.exists(cls.log.name):
            os.remove(cls.log.name)

    def test_pagina_de_uso(self):
        status, tipo, corpo = _get(self.base + "/")
        self.assertEqual(status, 200)
        self.assertIn("text/html", tipo)
        self.assertIn("Seu reajuste acompanhou a inflação?", corpo)

    def test_comparar_ok_com_virgula_decimal(self):
        url = self.base + "/comparar?preco_inicial=100,00&mes_inicial=2026-01&preco_final=105&mes_final=2026-03"
        status, _, corpo = _get(url)
        d = json.loads(corpo)
        self.assertEqual(status, 200)
        self.assertEqual(d["classificacao"], "acima")
        self.assertEqual(d["ipca_acumulado_pct"], 3.02)

    def test_entrada_invalida_retorna_400(self):
        casos = [
            "preco_inicial=0&mes_inicial=2026-01&preco_final=5&mes_final=2026-03",
            "preco_inicial=abc&mes_inicial=2026-01&preco_final=5&mes_final=2026-03",
            "preco_inicial=10&mes_inicial=2026-13&preco_final=5&mes_final=2026-03",
            "preco_inicial=10&mes_inicial=2026-03&preco_final=5&mes_final=2026-01",
            "preco_inicial=10&mes_inicial=2026-01&preco_final=5",
            "preco_inicial=10&mes_inicial=2025-01&preco_final=5&mes_final=2026-03",
        ]
        for q in casos:
            status, _, corpo = _get(self.base + "/comparar?" + q)
            self.assertEqual(status, 400, q)
            self.assertIn("erro", json.loads(corpo))

    def test_api1_continua_disponivel(self):
        status, _, corpo = _get(self.base + "/ipca?inicio=2026-02&fim=2026-03")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(corpo)["total"], 2)

    def test_rota_inexistente_retorna_404(self):
        status, _, _ = _get(self.base + "/nada")
        self.assertEqual(status, 404)

    def test_ref_e_registrado_no_log(self):
        url = self.base + "/comparar?preco_inicial=10&mes_inicial=2026-01&preco_final=11&mes_final=2026-03&ref=mercado-teste"
        _get(url)
        # O servidor grava o log depois de enviar a resposta; espera um instante.
        linhas = []
        for _ in range(50):
            if os.path.exists(api1.LOG_ACESSOS):
                with open(api1.LOG_ACESSOS, encoding="utf-8") as f:
                    linhas = list(csv.reader(f))
                if any(len(l) > 1 and l[1] == "mercado-teste" for l in linhas):
                    break
            time.sleep(0.1)
        self.assertEqual(linhas[0], ["timestamp_utc", "ref", "rota", "status"])
        self.assertTrue(any(l[1] == "mercado-teste" and l[2] == "/comparar" and l[3] == "200" for l in linhas[1:]))

    def test_head_responde_sem_corpo(self):
        req = urllib.request.Request(self.base + "/", method="HEAD")
        with urllib.request.urlopen(req) as r:
            self.assertEqual(r.status, 200)
            self.assertIn("text/html", r.headers.get("Content-Type", ""))
            self.assertEqual(r.read(), b"")
        req = urllib.request.Request(self.base + "/comparar", method="HEAD")
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req)
        self.assertEqual(ctx.exception.code, 405)

    def test_sem_ref_nao_registra(self):
        antes = os.path.getsize(api1.LOG_ACESSOS) if os.path.exists(api1.LOG_ACESSOS) else 0
        _get(self.base + "/ajuda")
        depois = os.path.getsize(api1.LOG_ACESSOS) if os.path.exists(api1.LOG_ACESSOS) else 0
        self.assertEqual(antes, depois)


if __name__ == "__main__":
    unittest.main()
