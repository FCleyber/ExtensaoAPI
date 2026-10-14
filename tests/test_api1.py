"""Testes da API 1. Rodar: python -m unittest test_api1 -v
Usam dados simulados no formato do SGS, então não dependem da internet."""
import json
import threading
import unittest
import urllib.error
import urllib.request

import api1

BRUTO = [
    {"data": "01/07/2026", "valor": "0.10"},
    {"data": "01/06/2026", "valor": "0.25"},
    {"data": "01/08/2026", "valor": "-0.32"},
]


def _get(url):
    try:
        with urllib.request.urlopen(url) as r:
            return r.status, json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))


class TestFuncoes(unittest.TestCase):
    def test_normalizar_converte_formato_e_ordena(self):
        dados = api1.normalizar(BRUTO)
        self.assertEqual([d["mes"] for d in dados], ["2026-06", "2026-07", "2026-08"])
        self.assertEqual(dados[-1], {"mes": "2026-08", "ipca_mensal_pct": -0.32})

    def test_ipca_negativo_vira_numero(self):
        self.assertEqual(api1.normalizar([{"data": "01/08/2026", "valor": "-0.32"}])[0]["ipca_mensal_pct"], -0.32)

    def test_filtrar_intervalo_inclusivo(self):
        dados = api1.normalizar(BRUTO)
        self.assertEqual([d["mes"] for d in api1.filtrar(dados, "2026-07", "2026-08")], ["2026-07", "2026-08"])
        self.assertEqual(len(api1.filtrar(dados)), 3)


class TestServidor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        api1._cache["dados"] = api1.normalizar(BRUTO)
        api1._cache["quando"] = 1e18  # cache nunca expira durante o teste
        cls.srv = api1.ThreadingHTTPServer(("127.0.0.1", 0), api1.Handler)
        cls.base = "http://127.0.0.1:%d" % cls.srv.server_address[1]
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()

    def test_ipca_completo(self):
        status, corpo = _get(self.base + "/ipca")
        self.assertEqual(status, 200)
        self.assertEqual(corpo["total"], 3)
        self.assertEqual(corpo["ultimo_mes_disponivel"], "2026-08")
        self.assertEqual(corpo["serie_sgs"], 433)

    def test_ipca_com_intervalo(self):
        status, corpo = _get(self.base + "/ipca?inicio=2026-07&fim=2026-08")
        self.assertEqual(status, 200)
        self.assertEqual(corpo["total"], 2)

    def test_formato_invalido_retorna_400(self):
        status, corpo = _get(self.base + "/ipca?inicio=2026-13")
        self.assertEqual(status, 400)
        self.assertIn("erro", corpo)

    def test_inicio_depois_do_fim_retorna_400(self):
        status, _ = _get(self.base + "/ipca?inicio=2026-08&fim=2026-01")
        self.assertEqual(status, 400)

    def test_rota_inexistente_retorna_404(self):
        status, _ = _get(self.base + "/nada")
        self.assertEqual(status, 404)

    def test_ajuda_na_raiz(self):
        status, corpo = _get(self.base + "/")
        self.assertEqual(status, 200)
        self.assertIn("rotas", corpo)


if __name__ == "__main__":
    unittest.main()
