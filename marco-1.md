# Entrega de marco — Marco 1

## Identificação

- **Equipe:** Samuel Luiz [567412], Diego Lopes [556906], Fernando Cleyber [564872]
- **Marco e data:** Marco 1, entrega remota até 04/10/2026
- **Trilha:** (A) API pública de dados abertos
- **Endereço público do produto:** n.a. neste marco (a publicação em endereço na internet é exigência do Marco 3). O produto roda localmente com o comando do `README.md`. Repositório: https://github.com/FCleyber/ExtensaoAPI
- **Commit ou tag desta entrega:** [PREENCHER: hash do commit que contém `api1.py`; aparece no GitHub ao lado do último commit]

## Campo 1 — O que funciona hoje

Requisito: Python 3.8+ e internet. Depois de `git clone https://github.com/FCleyber/ExtensaoAPI`, `cd ExtensaoAPI` e `python api1.py` (o terminal mostra `API 1 no ar`):

1. Abrir `http://127.0.0.1:8000/ipca` e receber em JSON a série mensal completa do IPCA (série 433 do SGS, desde 1980-01), cada item no formato `{"mes": "2026-08", "ipca_mensal_pct": -0.32}`.
2. Abrir `http://127.0.0.1:8000/ipca?inicio=2026-01&fim=2026-08` e receber só os meses desse intervalo; com formato inválido (por exemplo `?inicio=2026-13`) recebe HTTP 400 com a mensagem de erro.
3. Abrir `http://127.0.0.1:8000/` e ver a lista de rotas com um exemplo de uso.

Também roda `python -m unittest test_api1 -v` (9 testes, sem internet).

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

[COMPLETAR com o que realmente travou e quanto tempo custou. Pontos que aconteceram e podem entrar, se forem verdade para a equipe: os arquivos de entrega estavam dentro de `modelos/` e o plano estava em `.docx`; foram movidos para a raiz com os nomes oficiais e o plano foi convertido para `plano-de-acao.md` e revisado em 04/10; o escopo foi reduzido a comparar preço com IPCA, deixando o cálculo e a explicação para o Marco 2.]

## Campo 5 — Autopontuação

Pontuação conforme a rubrica do PDF `extensao/entrega-de-marco.pdf`. Nota = 10 × pontos obtidos / pontos aplicáveis.

| Dimensão | n.a.? | Pts (0–2) | Por quê, em uma linha |
| :-- | :-- | :-- | :-- |
| D1 Qualidade técnica | não | [PREENCHER] | [PREENCHER] |
| D2 Alcance e adequação ao público | sim | — | Ainda não há como existir neste marco. |
| D3 Documentação e reprodutibilidade | não | [PREENCHER] | [PREENCHER] |
| D4 Registro do processo | não | [PREENCHER] | [PREENCHER] |
| D5 Autoavaliação e reflexão | sim | — | Ainda não há como existir neste marco. |

## Antes de entregar

- [ ] O endereço do produto abre numa máquina que não é a nossa (n.a. neste marco; vale o clone limpo abaixo).
- [ ] O que o Campo 1 promete foi testado hoje, numa pasta limpa, seguindo só o `README.md`.
- [ ] O `README.md` corresponde ao que o produto faz agora.
- [ ] O diário tem entrada de todas as semanas desde o último marco.
- [ ] Toda evidência do Campo 3 tem data e está registrada em `evidencias.csv`.
- [ ] O commit informado está publicado.
