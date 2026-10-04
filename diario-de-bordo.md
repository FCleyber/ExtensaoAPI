# Diário de bordo

Registro semanal do trabalho da equipe (Samuel Luiz, Diego Lopes e Fernando Cleyber). Comprova as horas de execução autônoma e alimenta a dimensão D4 da rubrica.

---

## Entradas

### Semana de 07/09

**Quem trabalhou e quanto:** nenhuma atividade autônoma registrada nesta semana.

**O que foi feito:**
- Aula de sexta (11/09): o professor explicou o modelo do plano de ação, o que torna um projeto bom e as datas dos marcos.

**Obstáculo:** nenhum registrado.

**Contato com o público:** nenhum.

**Evidência coletada:** relato da aula repassado por Fernando no grupo da equipe em 14/09.

**Próxima semana:** reunir a equipe, escolher a trilha e começar o plano de ação.

---

### Semana de 14/09

**Quem trabalhou e quanto:** Samuel — cerca de 2h; Diego — cerca de 4h; Fernando — cerca de 2h30

**O que foi feito:**
- 14/09: grupo da equipe criado; combinada uma reunião e Fernando repassou as orientações da aula.
- 17/09: Diego e Fernando encontraram a pasta de modelos com o plano de ação. A equipe discutiu a trilha (API pública de dados abertos) e duas ideias: transporte público de Fortaleza (dados GTFS da ETUFOR) e indicadores macroeconômicos do Banco Central explicados em linguagem simples. Decidiu seguir com os dados do BACEN e manter o escopo pequeno, como o professor recomendou.
- 17 e 18/09: preenchimento do plano (matrículas, público externo, forma de divulgação) e decisão de enviar ao professor uma versão ainda incompleta para receber opinião.

**Obstáculo:** o escopo inicial estava grande demais (vários indicadores, preços de mercado, fiscalização). Foi reduzido na semana seguinte. Provas e compromissos pessoais limitaram o tempo de parte da equipe.

**Contato com o público:** nenhum com o público externo; houve troca de mensagens com o professor.

**Evidência coletada:** conversa do grupo da equipe e versão preliminar do plano de ação.

**Próxima semana:** responder ao e-mail do professor, criar o repositório e revisar o plano.

---

### Semana de 21/09

**Quem trabalhou e quanto:** Samuel — cerca de 2h30; Diego — cerca de 3h; Fernando — cerca de 3h30

**O que foi feito:**
- 21/09: o professor respondeu por e-mail pedindo para revisar o plano e fechar os pontos pendentes; Diego respondeu apresentando a ideia e o professor propôs uma call. Fernando criou o repositório ExtensaoAPI no GitHub, já com a pasta `modelos/`.
- 22/09: Diego fez a versão 2 do plano, com foco no consumidor comum; Fernando adicionou Samuel e Diego como colaboradores do repositório.
- 23/09: o professor respondeu ao e-mail de Diego.
- 25/09: Fernando propôs um plano de escopo menor e mais realista, com base na versão 2 e nas orientações do professor.
- 27/09: escopo reduzido a um relatório sobre o reajuste de preços comparado ao IPCA, sem os outros indicadores.
- Ao longo da semana: Samuel fez pesquisas na internet sobre o tema (cerca de 1h, espaçadas).

**Obstáculo:** a ideia estava ampla demais e difícil de tornar real; foi preciso reduzir o escopo. Parte da equipe ficou ausente em alguns dias por compromissos.

**Contato com o público:** nenhum com o público externo; e-mails com o professor.

**Evidência coletada:** repositório criado em 21/09 (histórico de commits), e-mails com o professor e versões do plano.

**Próxima semana:** call com o professor (Diego marcou para 28/09, 9h) e fechamento do plano.

---

### Semana de 28/09 (entrega do Marco 1 em 04/10)

**Quem trabalhou e quanto:** Samuel — cerca de 5h30; Diego — cerca de 1h30; Fernando — cerca de 3h

**O que foi feito:**
- 28 e 30/09: Diego marcou call com o professor; Samuel e Fernando tiveram compromissos e não puderam participar da de 30/09.
- 29/09: Fernando redigiu uma entrada de diário e seguiu atualizando o plano.
- 03/10: a equipe percebeu que o Marco 1 exigia também uma primeira versão do produto rodando, não só o plano.
- 04/10: plano de ação finalizado e convertido para `plano-de-acao.md` (Fernando preencheu as lacunas e publicou no repositório; revisão e ajustes feitos por Samuel com apoio do Claude). Dados da série 433 conferidos no SGS (IPCA, variação percentual mensal, fonte IBGE, desde 01/1980, último valor ago/2026 = −0,32%) e licença ODbL confirmada na página do conjunto no Portal de Dados Abertos do Banco Central.
- 04/10: repositório reorganizado, com `plano-de-acao.md`, `diario-de-bordo.md`, `evidencias.csv` e `marco-1.md` na raiz, com os nomes de `03-modelos`.
- 04/10: API 1 publicada (`api1.py`, em Python, sem dependências): devolve o IPCA mensal em JSON, com filtro por intervalo de meses e tratamento de erro. Acompanha `test_api1.py` (9 testes) e o `README.md` com o comando exato. O código foi elaborado por Samuel com apoio do Claude (IA) e revisado, executado e testado pela equipe. Teste feito a partir de um clone novo, no Windows com Python 3.11: a API respondeu em `http://127.0.0.1:8000/ipca` e os 9 testes passaram.
- 04/10: ficha `marco-1.md` preenchida.
- Ao longo da semana: Samuel seguiu com pesquisas na internet sobre o tema (cerca de 1h, espaçadas).

**Obstáculo:** só em 03/10 a equipe entendeu que o Marco 1 pedia o produto rodando; o trabalho técnico ficou concentrado em 04/10 (cerca de 4h). Os arquivos de entrega estavam em `modelos/`, o plano só existia em `.docx` e o código da API 1 não estava no repositório. Tudo resolvido em 04/10. Provas e compromissos pessoais reduziram a disponibilidade na semana.

**Contato com o público:** nenhum com o público externo.

**Evidência coletada:** saída dos 9 testes passando (04/10/2026) e histórico de commits do repositório.

**Próxima semana:** primeira rodada de contato com comerciantes de Fortaleza (até 11/10), registrando cada tentativa em `evidencias.csv`; começar a API 2 (cálculo da variação de preço e do IPCA acumulado).
