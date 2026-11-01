# ExtensaoAPI

Projeto de Extensão da cadeira Interfaces de Programação de Aplicação.

**Equipe:** Samuel Luiz [567412], Diego Lopes [556906], Fernando Cleyber [564872]

**O que é:** um serviço de APIs públicas que ajuda pequenos comerciantes de Fortaleza a comparar o reajuste de preço de um produto com a inflação (IPCA) do período. O plano completo está em [`plano-de-acao.md`](plano-de-acao.md).

## Estado atual

- **API 1 (pronta):** consulta o IPCA mensal no Banco Central e devolve os dados em JSON (rota `/ipca`).
- **API 2 e página de uso (prontas para o Marco 2):** comparam o reajuste de um produto com o IPCA acumulado e explicam o resultado em linguagem simples. O cálculo é feito em código; o texto padrão funciona sem chave de API, e o LLM é opcional (`src/llm/`).

## Como rodar o app completo (página de uso + API 2 + API 1)

**Requisitos:** Python 3.8 ou superior e acesso à internet. Não há nada para instalar.

```bash
git clone https://github.com/FCleyber/ExtensaoAPI
cd ExtensaoAPI
python src/api/api2.py
```

No Windows, se `python` não funcionar, use `py src/api/api2.py`. No Linux e no macOS, `python3 src/api/api2.py`.

Deixe o terminal aberto e acesse no navegador:

| O que você quer | Endereço |
| :-- | :-- |
| Página de uso (formulário) | http://127.0.0.1:8000/ |
| API 2: comparar um reajuste com o IPCA | http://127.0.0.1:8000/comparar?preco_inicial=10&mes_inicial=2026-01&preco_final=10,80&mes_final=2026-08 |
| API 1: série do IPCA | http://127.0.0.1:8000/ipca?inicio=2026-01&fim=2026-08 |
| Lista de rotas em JSON | http://127.0.0.1:8000/ajuda |

### Regra de cálculo da API 2

- **Variação do preço (%)** = (`preco_final` / `preco_inicial` − 1) × 100.
- **IPCA acumulado (%)** = (Π (1 + IPCA do mês / 100) − 1) × 100, do mês **seguinte** a `mes_inicial` até `mes_final`, inclusive. O mês inicial não entra, porque o preço inicial já incorpora a inflação dele.
- **Comparação:** diferença = variação do preço − IPCA acumulado. Até 1 ponto percentual (para mais ou para menos) é `proximo`; acima disso, `acima` ou `abaixo`.
- Preços aceitam vírgula (`10,80`). Meses no formato `AAAA-MM`, entre o primeiro e o último mês com dado do IPCA.
- Exemplo: R$ 10,00 para R$ 10,80 (+8,0%) com IPCA acumulado de 5,0% resulta em `acima`, 3,0 pontos percentuais.

Resposta de exemplo de `/comparar` (campos principais): `variacao_preco_pct`, `ipca_acumulado_pct`, `diferenca_pp`, `classificacao`, `meses_considerados`, `explicacao`, `fonte` e `aviso`.

Erros: entrada inválida (preço zero ou não numérico, mês fora do formato, `mes_final` não posterior ao inicial, mês sem dado) retorna HTTP 400 com `{"erro": "..."}`; Banco Central fora do ar retorna HTTP 502.

### LLM (opcional)

Por padrão a explicação sai de um texto-modelo, sem chave e sem instalar nada. Para ativar o LLM: instale as dependências de `requirements-opcional.txt`, defina `USAR_LLM_EXPLICACAO=1` e a chave do provedor (`ANTHROPIC_API_KEY` ou `GEMINI_API_KEY`) **como variável de ambiente**. Nunca coloque a chave no código nem no repositório. Se o LLM falhar, o texto-modelo é usado. O LLM só reescreve a frase; os números vêm sempre do código.

## Como rodar só a API 1## Como rodar a API 1

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
| `HOST` | Endereço em que o servidor escuta | `127.0.0.1` (só este computador); `0.0.0.0` quando a variável `PORT` existe, como na hospedagem |
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
| `src/api/api1.py` | Código da API 1 (IPCA em JSON) |
| `src/api/api2.py` | API 2 (comparação com o IPCA) e página de uso; também serve a API 1 |
| `src/llm/` | Módulo que escreve a explicação em linguagem simples (texto padrão sem chave; LLM opcional) |
| `coleta de dados/` | Script auxiliar de coleta do IPCA no SGS (usa a biblioteca `requests`) |
| `tests/` | Testes da API 1 e da API 2 (`test_api1.py`, `test_api2.py`) |
| `requirements-opcional.txt` | Dependências só do LLM opcional e do script de coleta |
| `modelos/` | Materiais da disciplina (modelos e guias) |

## Publicação (Render)

O app é publicado como *Web Service* no Render, a partir deste repositório:

- **Runtime:** Python 3. **Build Command:** deixar em branco (não há dependências). **Start Command:** `python src/api/api2.py`.
- Não é preciso definir variáveis: o Render fornece `PORT` e o app passa a escutar em todas as interfaces. Cada comerciante recebe um link com marcador próprio, por exemplo `https://<endereco-do-render>/?ref=nome-do-contato`; os acessos aparecem nos logs do serviço como linhas `ACESSO ...`.
- Endereço público: [PREENCHER após o deploy]
