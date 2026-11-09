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

### Semana 05/10 

Quem trabalhou e quanto: Diego - 5h; Samuel - 2,5h; Cleyber - 3h

O que foi feito:
 Diego - Estudos de modelos deterministico para saber quais modelos seriam mais apropiado como factor model e entre outros, algumas tecnicas de series temporais; exploração das bases de dados além do bacem, como o IBGE afim de encontrar mais fenomenos macroeconomico; criação do modulo `llm_cliente.py`, modulo dedicado para centralizar toda a comunicação do projeto com o LLM (Anthropic e GEMINI); Coleta de dados; criação do `schemas.py` pydantic para ter uma saida estruturadfa do llm para o modulo de narrativa e TXTs como pratica de eng de prompt para externalização do prompt do codigo

Samuel - Ambos focaram em formular perguntas para validar a ideia o conceito para o publico externo e foi feito uma conversa previa com um comerciante da cantina da quimica 
Cleyber - Ambos focaram em formular perguntas para validar a ideia o conceito para o publico externo e foi feito uma conversa previa com um comerciante da cantina da quimica 
 
** Obstaculos:** Durante o estudo, ter uma dimensão, compreensão das series que foram coletadas pelo SGS, erro 406 client error em algumas series que foram pontuadas como importante pela equipe. 
Séries com erro: ['selic', 'cdi', 'dolar']

**Proxima semana: ** Melhoria no codigo, Ampliar o numero de tentativas em coleta de dados de series, principalmente nas que derao erro durante a primeira coleta. Usar tecnica de mais tempo durante a requisição; Implementação de modelos deterministico; Interface no strealit e contato com o publico externo; modificações constantes nos arquivos txt conforme a versão do projeto
whas
## Semana de 12/10

Quem trabalhou e quanto: Diego — 4h ; Samuel — 1,5h; Cleyber — 1,5h

O que foi feito:

Diego: Corrigido o coletor pra só IPCA, cortadas as outras 13 séries fora do escopo. Módulo de LLM reduzido: ele não calcula nada, só reescreve o resultado pronto, com template padrão funcionando sem chave e LLM opcional por trás de uma flag, com fallback se falhar. E trocado os .txt vazios por um prompt só, de verdade, dentro de prompts/. Implementação na 'api1.py', função registrar acesso de cada chamada e implementação do log de chamadacom ?ref=

Samuel: contato com o publico
Cleyber: contato com o publico

Obstáculo: 
Diego: Nenhum.

Contato com o público: Contato com o público: Samuel e Cleyber fizeram contato com o público esta semana.


Próxima semana: deploy da API no Render; mais contato com comerciantes;


### Semana de 19/10 (registrada com atraso, em 01/11)

**Quem trabalhou e quanto:** Diego — não informado; Samuel — 0h; Cleyber — 0h

**O que foi feito:** Diego implementou o registro de acessos com `?ref=` na API 1 e ajustes no `api1.py` (commits de 19/10 e 24/10). Pouco avanço do restante da equipe, por provas e atividades de outras disciplinas.

**Contato com o público:** nenhum. **Obstáculo:** provas e atividades de outras disciplinas.

**Próxima semana:** voltar a procurar os comerciantes e retomar a API 2.

### Semana de 26/10

**Quem trabalhou e quanto:** Samuel — cerca de 4h (2h de pesquisa sobre deploy ao longo da semana e cerca de 2h em 01/11); Cleyber — 2h; Diego — não informado.

**O que foi feito:** Samuel e Cleyber visitaram o Mercado da Praça (28/10). Cleyber conversou com o Raimundo, que aceitou testar o produto (31/10), e organizou o `evidencias.csv` e os prints. Samuel pesquisou como publicar o app no Render, corrigiu o README e os testes, fez a API 2 e a página de uso, com apoio do Claude (IA), revisadas e testadas pela equipe, e publicou o app em https://extensaoapi.onrender.com (01/11).

**Contato com o público:** 3 registros em `evidencias.csv` (28/10 e 31/10). **Obstáculo:** o Mercado da Praça ainda não respondeu.

**Próxima semana:** testar com o Raimundo e a loja Tudo Limpo usando links com `?ref=` e registrar os acessos em `evidencias/`.

### Correções registradas em 01/11/2026

As entradas anteriores não foram reescritas, conforme orientação do professor. Corrigimos aqui:
- Semana de 05/10: a conversa prévia com um comerciante da cantina da química não ocorreu.
- Semana de 28/09: a call com o professor marcada para 30/09 não aconteceu.
- Semanas de 07/09 a 28/09: as entradas foram reconstruídas em 04/10, a partir do grupo da equipe, dos e-mails e do repositório, como declarado na ficha do Marco 1.
=======
### Semana de 02/11

**Quem trabalhou e quanto:** Samuel — cerca de 4h; Cleyber — [horas dele ou "não informado"]; Diego — [horas dele ou "não informado"]

**O que foi feito:** Samuel acrescentou ao app uma cópia de reserva do IPCA para quando o Banco Central não responder, o limite de 5 anos no período e a exibição do período na página, com 5 testes novos (31 no total), e publicou a nova versão no Render.

**Contato com o público:** nenhum nesta semana; a visita e o teste com os comerciantes não aconteceram por falta de tempo da equipe.

**Próxima semana:** enviar os links com `?ref=` ao Raimundo e à loja Tudo Limpo, e preparar a ficha do Marco 2 (13/11).
Quem trabalhou e quanto: Diego ;
>>>>>>> Stashed changes
