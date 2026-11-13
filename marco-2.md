# Entrega de marco — Marco 2

## Identificação

- **Equipe:** Samuel Luiz [567412], Diego Lopes [556906], Fernando Cleyber [564872]
- **Marco e data:** Marco 2, 13/11/2026
- **Trilha:** (A) API pública de dados abertos
- **Endereço público do produto:** https://extensaoapi.onrender.com (publicado no Render em 01/11/2026)
- **Commit ou tag desta entrega:** tag `marco-2`, que aponta para o último commit desta entrega

O plano gratuito do Render "dorme" quando fica sem uso: a primeira abertura pode levar perto de um minuto.

## Campo 1 — O que funciona hoje

1. Abrir https://extensaoapi.onrender.com, preencher R$ 10,00 em janeiro de 2026 e R$ 10,80 em agosto de 2026 e clicar em **Comparar**. A página mostra: "O reajuste de 8,0% ficou acima da inflação do período (2,8%), uma diferença de 5,2 pontos percentuais", com a variação do preço (8%), o IPCA do período (2,77%), a diferença (5,23 pontos) e a linha "Inflação somada de fev/2026 a ago/2026 (7 meses)".
2. Abrir https://extensaoapi.onrender.com/comparar?preco_inicial=10&mes_inicial=2026-01&preco_final=10,80&mes_final=2026-08 e receber o mesmo resultado em JSON (`variacao_preco_pct: 8.0`, `ipca_acumulado_pct: 2.77`, `diferenca_pp: 5.23`, `classificacao: "acima"`, período considerado e explicação). Com dado inválido, por exemplo um período acima de 5 anos, a resposta é HTTP 400 com a mensagem do erro.
3. Abrir https://extensaoapi.onrender.com/ipca?inicio=2026-01&fim=2026-08 e receber em JSON os 8 meses do IPCA (série 433 do SGS), com a fonte e o último mês disponível.

Também funciona no computador, sem instalar nada: `git clone https://github.com/FCleyber/ExtensaoAPI`, `cd ExtensaoAPI` e `python src/api/api2.py`, abrindo `http://127.0.0.1:8000/`. Os testes rodam com `python -m unittest discover -s tests -v` (31 testes, sem internet).

## Campo 2 — O que mudou desde o marco anterior

- **Passou a existir:**
  - API 2: cálculo determinístico da variação do preço e do IPCA acumulado (do mês seguinte ao inicial até o final), comparação (acima, abaixo ou próximo, com limiar de 1 ponto percentual) e explicação em linguagem simples. O texto padrão funciona sem chave de API; o LLM é opcional e só reescreve a frase, nunca calcula.
  - Página de uso com formulário de quatro campos, feita para celular, com números em vírgula e o período considerado.
  - Publicação no Render em 01/11, antecipada do Marco 3 para antes do Marco 2, como o professor orientou.
  - Registro de acessos com o marcador `?ref=` de cada comerciante, nos logs do Render.
  - Cópia de reserva do IPCA (`dados/ipca_reserva.json`), usada se o Banco Central não responder, e limite de 5 anos no período.
  - Testes: de 9 (Marco 1) para 31, incluindo casos conferidos à mão.
  - Primeiro uso externo, em 13/11, durante a visita da equipe aos comerciantes para testar a API 2 (Campo 3).
- **Foi cortado, e por quê:**
  - A coleta de 14 séries (Selic, dólar, desemprego, dívida pública) e o uso do LLM para explicar "fenômenos macroeconômicos": saíam do plano de 04/10, que é comparar um reajuste com o IPCA. Foram cortados em 14/10, depois da orientação do professor.
  - Modelos de séries temporais e regressão: não cabiam no escopo combinado e não entraram.
  - Interface em Streamlit: a página foi feita em HTML simples, servida pelo próprio app, para não exigir instalação nem dependências.

## Campo 3 — Alcance

| Indicador | Planejado | Obtido até hoje | Onde está a evidência |
| :-- | :-- | :-- | :-- |
| Chamadas externas à API 2, por link com `ref` | Pelo menos 10, de pelo menos 2 marcadores (até o Marco 3) | 7 chamadas de 2 marcadores (raimundo: 3; mercado-da-praca: 4), 2 com resultado e 5 com erro de entrada, na visita da equipe em 13/11. A loja Tudo Limpo abriu a página 2 vezes, sem comparar. | `evidencias/2026-11-13-acessos-render.txt`, `evidencias/2026-11-13-logs-render.pdf` (tela do Render) e `evidencias.csv` (13/11) |
| Respostas sobre a compreensão do resultado | Pelo menos 2 afirmativas, ou 3 tentativas documentadas (até o Marco 3) | 2 respostas afirmativas (Raimundo e Mercado da Praça), dadas pessoalmente na visita de 13/11 e anotadas pela equipe: os dois disseram que entenderam o resultado e que a ferramenta pode ser muito útil para ajustar os preços. Meta atingida. Desde 09/10 há 11 registros de contato com 3 comerciantes. | `evidencias.csv` (13/11) e prints em `evidencias/` |

**O que o público externo disse.** Na visita de 13/11, depois de comparar os preços que praticaram em alguns produtos desde o começo do ano, os comerciantes que testaram disseram que entenderam se o preço subiu acima, abaixo ou próximo da inflação e que a ferramenta pode ser muito útil para ajustar os preços nos meses seguintes (respostas dadas pessoalmente, anotadas pela equipe). Antes, em 12/10, a dona da loja Tudo Limpo já tinha respondido "Sim. Seria bem positivo." à pergunta sobre a utilidade de uma ferramenta assim. Até o Marco 3, vamos pedir a cada um a confirmação por escrito e voltar com a correção dos meses (Campo 4).

## Campo 4 — Obstáculo e replanejamento

- **5 das 7 comparações externas deram erro de entrada.** Os comerciantes quiseram comparar do começo do ano até hoje, mas o mês atual e os seguintes ainda não têm IPCA divulgado; houve também um período acima de 5 anos e um mês final antes do inicial. A página não informa até que mês há dados. Replanejamento até o Marco 3: mostrar na página o último mês disponível, impedir a escolha de meses sem dado e escrever as mensagens de erro em linguagem simples.
- **O uso externo ficou para o dia da entrega.** A visita e o teste com os comerciantes previstos para a semana de 02/11 não aconteceram por falta de tempo da equipe. A equipe toda fez a visita em 13/11 (cerca de 4h de deslocamento e teste) e entregou os links nesse dia. Replanejamento: voltar aos três comerciantes na semana de 16/11, já com a correção dos meses, e fazer a pergunta sobre a compreensão do resultado.
- **O deploy atrasou.** Estava previsto para 18/10 e saiu em 01/11. Ainda assim, ficou antes do Marco 2, como o professor pediu.
- **Registro do processo.** A semana de 19/10 foi registrada com atraso, em 01/11, e as correções de entradas antigas foram feitas numa entrada nova, sem reescrever as anteriores. Desde 26/10, as entradas são escritas na própria semana.

## Campo 5 — Autopontuação

Pontuação conforme a rubrica do PDF `extensao/entrega-de-marco.pdf`. Nota = 10 × pontos obtidos / pontos aplicáveis.

| Dimensão | n.a.? | Pts (0–2) | Por quê, em uma linha |
| :-- | :-- | :-- | :-- |
| D1 Qualidade técnica | não | 2 | Funciona de ponta a ponta no endereço público, com dados reais do Banco Central, cálculo determinístico, cópia de reserva e 31 testes passando. |
| D2 Alcance e adequação ao público | não | 2 | Dois comerciantes usaram o produto com seus próprios preços, disseram que entenderam o resultado e o acharam útil|
| D3 Documentação e reprodutibilidade | não | 2 | O README traz o endereço público, os comandos para rodar e testar, a regra de cálculo e as instruções de publicação, e foi seguido em um clone limpo. |
| D4 Registro do processo | não | 2 | Há entrada para todas as semanas desde o Marco 1 e correções registradas sem reescrever o passado. |
| D5 Autoavaliação e reflexão | sim | — | A autoavaliação individual é em 04/12. |

## Antes de entregar

- [x] O endereço do produto abre numa máquina que não é a nossa.
- [x] O que o Campo 1 promete foi testado hoje, não na semana passada.
- [x] O `README.md` corresponde ao que o produto faz agora.
- [x] O diário tem entrada de todas as semanas desde o último marco.
- [x] Toda evidência do Campo 3 tem data e está em `evidencias/`.
- [x] O commit informado está publicado (tag `marco-2`).
