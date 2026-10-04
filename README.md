# ExtensaoAPI

Projeto de Extensão da cadeira Interfaces de Programação de Aplicação.

**Equipe:** Samuel Luiz [567412], Diego Lopes [556906], Fernando Cleyber [564872]

**O que é:** um serviço de APIs públicas que ajuda pequenos comerciantes de Fortaleza a comparar o reajuste de preço de um produto com a inflação (IPCA) do período. O plano completo está em [`plano-de-acao.md`](plano-de-acao.md).

## Estado atual (Marco 1)

Existe a **API 1**: consulta o IPCA mensal no Banco Central e devolve os dados em JSON. A API 2 (cálculo e comparação) e a página de uso são do Marco 2.

## Como rodar a API 1

**Requisitos:** Python 3.8 ou superior e acesso à internet. Não há nada para instalar.

```bash
git clone https://github.com/FCleyber/ExtensaoAPI
cd ExtensaoAPI
python api1.py
```

No Windows, se `python` não funcionar, use `py api1.py`. No Linux e no macOS, `python3 api1.py`.

O terminal mostra `API 1 no ar: http://127.0.0.1:8000/ipca`. Deixe-o aberto e acesse no navegador (ou com `curl`):

| O que você quer | Endereço |
| :-- | :-- |
| Ajuda e lista de rotas | http://127.0.0.1:8000/ |
| Série completa do IPCA mensal (desde 1980-01) | http://127.0.0.1:8000/ipca |
| Só um intervalo de meses (inclusive) | http://127.0.0.1:8000/ipca?inicio=2026-01&fim=2026-08 |

Exemplo com `curl`:

```bash
curl "http://127.0.0.1:8000/ipca?inicio=2026-08&fim=2026-08"
```

Resposta:

```json
{
  "fonte": "IPCA, produzido pelo IBGE e disponibilizado pelo Banco Central do Brasil (SGS, série 433)",
  "serie_sgs": 433,
  "unidade": "variação percentual mensal",
  "ultimo_mes_disponivel": "2026-08",
  "total": 1,
  "dados": [
    { "mes": "2026-08", "ipca_mensal_pct": -0.32 }
  ]
}
```

(`ultimo_mes_disponivel` muda quando o IBGE divulga um novo mês.)

Para parar o servidor, use `Ctrl+C`. Para mudar a porta: `PORT=9000 python api1.py` (Linux/macOS) ou, no PowerShell, `$env:PORT=9000; python api1.py`.

### Erros

| Situação | Resposta |
| :-- | :-- |
| `inicio` ou `fim` fora do formato `AAAA-MM`, ou `inicio` depois de `fim` | HTTP 400 com `{"erro": "..."}` |
| Rota que não existe | HTTP 404 |
| Banco Central fora do ar ou sem internet | HTTP 502 com mensagem |

## Testes

```bash
python -m unittest test_api1 -v
```

Os testes usam dados simulados e não precisam de internet.

## Fonte dos dados e licença

- **Dados:** IPCA (variação percentual mensal), produzido pelo IBGE e disponibilizado pelo Banco Central do Brasil no Sistema Gerenciador de Séries Temporais (SGS), série 433.
- **Consulta usada:** `https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json`
- **Licença:** o conjunto é disponibilizado no Portal de Dados Abertos do Banco Central sob a Open Data Commons Open Database License (ODbL). Toda resposta da API cita a fonte.
- Os resultados são informativos e não substituem orientação econômica ou profissional.

## Organização do repositório

| Arquivo | Para quê |
| :-- | :-- |
| `plano-de-acao.md` | Plano de ação final |
| `marco-1.md` | Ficha de entrega do Marco 1 |
| `diario-de-bordo.md` | Registro semanal do trabalho |
| `evidencias.csv` | Evidências de contato com o público externo |
| `api1.py` | Código da API 1 |
| `test_api1.py` | Testes da API 1 |
| `modelos/` | Materiais da disciplina (modelos e guias) |
