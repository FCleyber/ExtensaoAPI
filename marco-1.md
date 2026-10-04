# Entrega de marco — Marco 1

## Identificação

- **Equipe:** Samuel Luiz [567412], Diego Lopes [556906], Fernando Cleyber [564872]
- **Marco e data:** Marco 1, entrega remota até 04/10/2026
- **Trilha:** (A) API pública de dados abertos
- **Endereço público do produto:** n.a. neste marco (a publicação em endereço na internet é exigência do Marco 3). O produto roda localmente com o comando do `README.md`. Repositório: https://github.com/FCleyber/ExtensaoAPI
- **Commit ou tag desta entrega:** [PREENCHER: hash de 7 caracteres do commit "Marco 1: API 1, README e ficha preenchida", visível na página principal do repositório]

## Campo 1 — O que funciona hoje

Requisito: Python 3.8+ e internet. Depois de `git clone https://github.com/FCleyber/ExtensaoAPI`, `cd ExtensaoAPI` e `python api1.py` (o terminal mostra `API 1 no ar`):

1. Abrir `http://127.0.0.1:8000/ipca` e receber em JSON a série mensal completa do IPCA (série 433 do SGS, desde 1980-01), cada item no formato `{"mes": "2026-08", "ipca_mensal_pct": -0.32}`.
2. Abrir `http://127.0.0.1:8000/ipca?inicio=2026-01&fim=2026-08` e receber só os meses desse intervalo; com formato inválido (por exemplo `?inicio=2026-13`) recebe HTTP 400 com a mensagem de erro.
3. Abrir `http://127.0.0.1:8000/` e ver a lista de rotas com um exemplo de uso.

Também roda `python -m unittest test_api1 -v` (9 testes, sem internet). Os três itens e os testes foram executados em 04/10/2026, a partir de um clone novo do repositório, no Windows 10 com Python 3.11.

## Campo 2 — O que mudou desde o marco anterior

n.a.

## Campo 3 — Alcance

Neste marco ainda não há contato com o público externo; o `evidencias.csv` está sem linhas porque não há evidência a registrar.

| Indicador | Planejado | Obtido até hoje | Onde está a evidência |
| :-- | :-- | :-- | :-- |
| Chamadas à API 2 | mais de 20 (até o Marco 3) | 0 (a API 2 é do Marco 2) | n.a. |
| Respostas de comerciantes sobre a compreensão da comparação | pelo menos 2 (até o Marco 3) | 0 | n.a. |

**O que o público externo disse.** Ninguém ainda. O plano para mudar isso: primeira rodada de contato com comerciantes de Fortaleza até 11/10/2026 e segunda até 25/10/2026, com cada tentativa registrada em `evidencias.csv` e no diário, conforme o `plano-de-acao.md`.

## Campo 4 — Obstáculo e replanejamento

- **Estrutura do repositório.** Os modelos estavam dentro de `modelos/` e o plano de ação existia apenas como `.docx`. Como a avaliação é feita pelo repositório, em 04/10 movemos `plano-de-acao.md`, `diario-de-bordo.md`, `evidencias.csv` e `marco-1.md` para a raiz, com os nomes de `03-modelos`, e convertemos o plano para Markdown. Resolvido.
- **Produto fora do repositório.** O código da API 1 ainda não estava publicado. Em 04/10 foram publicados `api1.py`, `test_api1.py` e o `README.md` com o comando exato, e o conjunto foi testado a partir de um clone novo. Resolvido.
- **Contato com o público ainda não iniciado.** Replanejamos o cronograma: a primeira rodada passou de 18/10 para até 11/10, e o primeiro contato será um convite para conversar sobre como o comerciante reajusta preços, que não depende do produto estar pronto.
- **Tempo gasto:** [PREENCHER: horas aproximadas em 04/10 com esses ajustes]

## Campo 5 — Autopontuação

Pontuação conforme a rubrica do PDF `extensao/entrega-de-marco.pdf`. Nota = 10 × pontos obtidos / pontos aplicáveis.

| Dimensão | n.a.? | Pts (0–2) | Por quê, em uma linha |
| :-- | :-- | :-- | :-- |
| D1 Qualidade técnica | não | 2 | A API 1 responde com dados reais do SGS, valida parâmetros (HTTP 400, 404 e 502) e tem 9 testes automatizados passando. |
| D2 Alcance e adequação ao público | sim | — | Ainda não há como existir neste marco. |
| D3 Documentação e reprodutibilidade | não | 2 | O README traz requisitos, comando exato e exemplo de resposta, e foi seguido em um clone novo, no Windows, em 04/10. |
| D4 Registro do processo | não | 1 | O diário cobre as semanas desde 07/09, mas parte das entradas foi completada na entrega, não no dia, e ainda não há evidências de contato. |
| D5 Autoavaliação e reflexão | sim | — | Ainda não há como existir neste marco. |

- [x] Toda evidência do Campo 3 tem data e está registrada em `evidencias.csv` (não há evidências ainda).
- [ ] O commit informado está publicado.
