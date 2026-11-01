# ExtensaoAPI

Projeto de Extensão da cadeira Interfaces de Programação de Aplicação.

**Equipe:** Samuel Luiz [567412], Diego Lopes [556906], Fernando Cleyber [564872]

**O que é:** um serviço de APIs públicas que ajuda pequenos comerciantes de Fortaleza a comparar o reajuste de preço de um produto com a inflação (IPCA) do período. O plano completo está em [`plano-de-acao.md`](plano-de-acao.md).

## Estado atual

- **API 1 (pronta):** consulta o IPCA mensal no Banco Central e devolve os dados em JSON. É a que se executa seguindo este README.
- **Em andamento (Marco 2):** a API 2, que calcula o IPCA acumulado e compara com o reajuste, e a página de uso. Já existe o módulo que escreve a explicação em linguagem simples (`src/llm/`), com texto padrão que funciona sem chave de API.

## Como rodar a API 1

**Requisitos:** Python 3.8 ou superior e acesso à internet. Não há nada para instalar.

```bash
git clone https://github.com/FCleyber/ExtensaoAPI
cd ExtensaoAPI
python src/api/api1.py
```

No Windows, se `python` não funcionar, use `py src/api/api1.py`. No Linux e no macOS, `python3 src/api/api1.py`.

O terminal mostra `API 1 no ar: http://0.0.0.0:8000/ipca`. Isso significa que o servidor está escutando; no navegador (ou com `curl`), use sempre o endereço `127.0.0.1`. Deixe o terminal aberto:

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

Para parar o servidor, use `Ctrl+C`.

### Configurações opcionais (variáveis de ambiente)

| Variável | Para quê | Padrão |
| :-- | :-- | :-- |
| `PORT` | Porta do servidor | `8000` |
| `HOST` | Endereço em que o servidor escuta. Use `127.0.0.1` para aceitar só conexões deste computador | `0.0.0.0` |
| `LOG_ACESSOS` | Arquivo onde os acessos com `?ref=` são registrados | `acessos.csv` |

Exemplos: no Linux e no macOS, `PORT=9000 HOST=127.0.0.1 python src/api/api1.py`. No PowerShell, `$env:PORT=9000; $env:HOST="127.0.0.1"; python src/api/api1.py`.

### Identificar quem acessa (`?ref=`)

Qualquer rota aceita o parâmetro `ref`, por exemplo `http://127.0.0.1:8000/ipca?ref=mercado-a`. Quando ele está presente, o acesso é registrado (data e hora em UTC, `ref`, rota e status) em `acessos.csv` e também impresso no terminal. A equipe usa isso para saber qual contato gerou qual uso, entregando um link com `ref` próprio a cada pessoa.

### Erros

| Situação | Resposta |
| :-- | :-- |
| `inicio` ou `fim` fora do formato `AAAA-MM`, ou `inicio` depois de `fim` | HTTP 400 com `{"erro": "..."}` |
| Rota que não existe | HTTP 404 |
| Banco Central fora do ar ou sem internet | HTTP 502 com mensagem |

## Testes

Na raiz do repositório:

```bash
python -m unittest discover -s tests -v
```

Os testes usam dados simulados e não precisam de internet.

## Fonte dos dados e licença

- **Dados:** IPCA (variação percentual mensal), produzido pelo IBGE e disponibilizado pelo Banco Central do Brasil no Sistema Gerenciador de Séries Temporais (SGS), série 433.
- **Consulta usada:** `https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json`
- **Licença:** o conjunto é disponibilizado no Portal de Dados Abertos do Banco Central sob a Open Data Commons Open Database License (ODbL). Toda resposta da API cita a fonte.
- Os resultados são informativos e não substituem orientação econômica ou profissional.

## Organização do repositório

| Caminho | Para quê |
| :-- | :-- |
| `plano-de-acao.md` | Plano de ação final |
| `docs/marco-1.md` | Ficha de entrega do Marco 1 |
| `diario-de-bordo.md` | Registro semanal do trabalho |
| `evidencias.csv` e `evidencias/` | Registro e comprovantes dos contatos com o público externo |
| `src/api/api1.py` | Código da API 1 |
| `src/llm/` | Módulo que escreve a explicação em linguagem simples (texto padrão sem chave; LLM opcional) |
| `coleta de dados/` | Script auxiliar de coleta do IPCA no SGS (usa a biblioteca `requests`) |
| `tests/test_api1.py` | Testes da API 1 |
| `modelos/` | Materiais da disciplina (modelos e guias) |
