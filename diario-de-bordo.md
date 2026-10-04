# Diário de bordo

Registro semanal do trabalho da equipe (Samuel Luiz, Diego Lopes e Fernando Cleyber). Comprova as horas de execução autônoma e alimenta a dimensão D4 da rubrica.

**Nota de honestidade:** as entradas de 07/09 a 28/09 foram completadas em 04/10/2026, a partir do histórico do repositório e da memória da equipe, e não no dia. As entradas seguintes serão escritas na própria semana.

---

## Entradas

### Semana de 07/09

**Quem trabalhou e quanto:** [PREENCHER: nome — Xh; nome — Xh]

**O que foi feito:**
- Escolha do tema (inflação e reajuste de preços para pequenos comerciantes) e da trilha A (API pública de dados abertos).
- Rascunho do plano de ação, datado de 11/09.

**Obstáculo:** [PREENCHER ou escrever "nenhum"]

**Contato com o público:** nenhum.

**Evidência coletada:** rascunho do plano de ação (versão em `.docx`, depois convertida para `plano-de-acao.md`).

**Próxima semana:** [PREENCHER]

---

### Semana de 14/09

**Quem trabalhou e quanto:** [PREENCHER: nome — Xh; nome — Xh]

**O que foi feito:**
- [PREENCHER o que foi feito; se nada andou, escrever isso]

**Obstáculo:** [PREENCHER ou escrever "nenhum"]

**Contato com o público:** nenhum.

**Evidência coletada:** nenhuma.

**Próxima semana:** [PREENCHER]

---

### Semana de 21/09

**Quem trabalhou e quanto:** [PREENCHER: nome — Xh; nome — Xh]

**O que foi feito:**
- Os modelos da disciplina (pasta `modelos/`) foram adicionados ao repositório.
- [PREENCHER qualquer outra coisa que tenha sido feita nesta semana]

**Obstáculo:** [PREENCHER ou escrever "nenhum"]

**Contato com o público:** nenhum.

**Evidência coletada:** histórico de commits do repositório (modelos adicionados por upload nesta semana).

**Próxima semana:** fechar o plano de ação e preparar o Marco 1.

---

### Semana de 28/09 (entrega do Marco 1 em 04/10)

**Quem trabalhou e quanto:** [PREENCHER: nome — Xh; nome — Xh]

**O que foi feito:**
- Plano de ação finalizado e convertido para `plano-de-acao.md`: dados da série 433 do SGS conferidos no próprio SGS (IPCA, variação percentual mensal, fonte IBGE, disponível desde 01/1980, último valor ago/2026 = −0,32%) e licença ODbL confirmada na página do conjunto no Portal de Dados Abertos do Banco Central.
- Escopo, regra de cálculo, cronograma e indicadores revisados no plano; primeira rodada de contato antecipada de 18/10 para até 11/10.
- Repositório reorganizado: `plano-de-acao.md`, `diario-de-bordo.md`, `evidencias.csv` e `marco-1.md` movidos para a raiz, com os nomes de `03-modelos`.
- API 1 publicada (`api1.py`, em Python, sem dependências): devolve o IPCA mensal em JSON, com filtro por intervalo de meses e tratamento de erro. Acompanha `test_api1.py` (9 testes) e o `README.md` com o comando exato. O código foi elaborado com apoio do Claude (IA) e revisado, executado e testado pela equipe.
- Teste feito a partir de um clone novo do repositório, no Windows com Python 3.11: a API respondeu em `http://127.0.0.1:8000/ipca` e os 9 testes passaram.
- Ficha `marco-1.md` preenchida.

**Obstáculo:** os arquivos de entrega estavam dentro de `modelos/`, o plano só existia em `.docx` e o código da API 1 não estava no repositório. Tudo resolvido em 04/10.

**Contato com o público:** nenhum ainda.

**Evidência coletada:** saída dos 9 testes passando (04/10/2026) e histórico de commits do repositório.

**Próxima semana:** primeira rodada de contato com comerciantes de Fortaleza (até 11/10), registrando cada tentativa em `evidencias.csv`; começar a API 2 (cálculo da variação de preço e do IPCA acumulado).

---

## O que conta como evidência
| Serve | Não serve |
| :-- | :-- |
| Mensagem de alguém de fora que usou | Captura de tela rodando na sua máquina |
| Registro de acessos ao endereço público | "Divulgamos nas redes", sem número |
| Lista de presença ou inscrição em oficina | Retorno de colega da própria turma |
| Retorno escrito, mesmo curto | Número coletado uma vez, no dia da apresentação |

Guarde as evidências no repositório, com data no nome do arquivo.
