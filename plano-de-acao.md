# Plano de ação

Rascunho em 11/09, versão final no Marco 1 (entrega remota, prazo 04/10).

## Identificação

- **Equipe:** Samuel Luiz [567412], Diego Lopes [556906], Fernando Cleyber [564872]
- **Trilha:** (A) API pública de dados abertos
- **Área temática da PREX:** Direitos Humanos e Justiça**
- **Por que essa área, em uma linha:** Dados públicos de inflação podem ajudar pequenos comerciantes a compreender se os reajustes de preços acompanharam ou ficaram acima/abaixo da inflação do período.
- **Repositório:** https://github.com/FCleyber/ExtensaoAPI

## Campo 1 — O problema

Um pequeno comerciante que precisa reajustar o preço de um produto não consegue comparar de forma simples o aumento aplicado com a inflação acumulada no mesmo período.

## Campo 2 — O público externo

- **Quem é:** Pequenos comerciantes locais de Fortaleza que realizam reajustes de preços e têm interesse em compreender sua relação com a inflação, sem necessidade de conhecimento técnico em economia.
- **Duas ou três pessoas reais desse grupo:** Pelo menos três comerciantes locais, a serem contatados pela equipe (nomes e meio de contato registrados em `evidencias.csv` a cada tentativa).
- **Já falamos com alguma? Quando falaremos?** Ainda não. O primeiro contato **não depende do produto**: será um convite para uma conversa curta sobre como o comerciante decide e aplica reajustes, o que também valida o problema do Campo 1. Cronograma de tentativas, uma por comerciante em cada rodada:
  - 1ª rodada: **até 11/10/2026**
  - 2ª rodada (nova tentativa a quem não respondeu, e convite para testar a página do produto a quem respondeu): **até 25/10/2026**
  - 3ª rodada, já com o produto utilizável (Marco 2): **entre 14/11 e 22/11/2026**

  Toda tentativa (convite enviado, e-mail, mensagem sem resposta) vira uma linha em `evidencias.csv` e uma entrada no `diario-de-bordo.md`, independentemente de haver resposta.
- **Como essa pessoa vai descobrir que o produto existe:** Por meio de contato direto da equipe e, posteriormente, pela divulgação em canais de entidades estudantis e redes sociais relacionadas a negócios, economia e empreendedorismo.

## Campo 3 — Trilha e produto

- **O que é, em uma frase que caiba num tuíte, e onde ficará publicado:** Um serviço de APIs públicas que consulta o IPCA e permite comparar a variação do preço de um produto com a inflação acumulada em um período, apresentando o resultado em linguagem simples. O código ficará no repositório público da equipe e o serviço será **publicado num endereço na internet até o Marco 3** (hospedagem a ser confirmada pela equipe até o Marco 2; candidatas: Render, Railway ou Cloudflare Workers, todas com plano gratuito).

O produto será desenvolvido em etapas:

- **API 1 (Marco 1):** consulta o IPCA mensal disponibilizado pelo Banco Central e retorna os dados em JSON de forma organizada. O README do repositório traz o comando exato para executá-la.
- **API 2 (Marco 2):** recebe preço inicial, preço final e dois meses de referência, calcula a variação do preço e o IPCA acumulado, compara os resultados e gera uma explicação em linguagem simples.
- **Página de uso (Marco 2):** uma página web mínima, com formulário de quatro campos, que chama a API 2. É por ela que o comerciante usará o produto, já que o público-alvo não consome JSON.

### Regra de cálculo (definição única, usada pela API 2 e pelos testes)

- **Entradas:** `preco_inicial`, `mes_inicial`, `preco_final`, `mes_final` (formato `AAAA-MM`).
- **Validações:** `preco_inicial` > 0; `mes_final` posterior a `mes_inicial`; ambos entre 1980-01 e o último mês disponível na série (hoje, 2026-08). Fora disso, a API retorna erro claro em vez de calcular.
- **Variação do preço (%)** = (`preco_final` / `preco_inicial` − 1) × 100.
- **IPCA acumulado (%)** = (Π (1 + IPCA_m / 100) − 1) × 100, com m variando do mês **seguinte** a `mes_inicial` até `mes_final`, **inclusive**. O mês inicial não entra, porque o preço inicial já incorpora a inflação daquele mês.
- **Comparação:** a variação do preço é classificada como *acima*, *próxima* ou *abaixo* do IPCA acumulado. "Próxima" significa diferença absoluta de até 1 ponto percentual (limiar ajustável, documentado no README).
- **Exemplo:** preço de R$ 10,00 para R$ 10,80 (+8,0%) entre dois meses cujo IPCA acumulado no intervalo foi 5,0% → o reajuste ficou **acima** da inflação em 3,0 pontos percentuais.

### Papel do LLM

O LLM **nunca calcula**: todos os números vêm do código. Ele apenas reescreve o resultado em linguagem simples. A explicação padrão é gerada por **template determinístico**, para que o produto funcione em qualquer máquina sem chave de acesso; o LLM é opcional e só é ativado se a variável de ambiente correspondente estiver configurada.

### O que NÃO faz parte

- Determinar preço ideal para produtos.
- Recomendar decisões financeiras ou comerciais individuais.
- Prever preços futuros.
- Estabelecer relação de causa e efeito entre inflação e o preço de um produto específico.
- Fazer análise contábil ou financeira de empresas.
- Utilizar dados da CVM, como DFP ou ITR.
- Analisar décadas de histórico.
- Explicar todas as causas da inflação.
- Utilizar outros indicadores macroeconômicos inicialmente, caso não sejam necessários ao produto.
- Substituir orientação econômica ou profissional.

## Campo 4 — Fontes de dados

| | |
|---|---|
| **Nome e órgão** | IPCA (Índice Nacional de Preços ao Consumidor Amplo), produzido pelo IBGE e disponibilizado pelo Banco Central do Brasil no Sistema Gerenciador de Séries Temporais (SGS). Série **433** (variação percentual mensal). |
| **Endereço** | `https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json` (consulta da série 433 no SGS: https://www3.bcb.gov.br/sgspub/consultarvalores/consultarValoresSeries.do?method=consultarSeries&series=433) |
| **Licença — e o que ela permite ao nosso produto** | O conjunto de dados da série 433 é disponibilizado no Portal de Dados Abertos do Banco Central sob a Open Data Commons Open Database License (ODbL), conforme exibido na página do conjunto (verificado em 04/10/2026). A licença permite utilizar, copiar, transformar e distribuir a base, observadas as condições de atribuição e compartilhamento. O projeto identificará o IBGE como produtor do índice e o Banco Central como fonte de acesso, e observará esses requisitos caso dados ou bases derivadas sejam redistribuídos. |
| **Atualização — periodicidade declarada e data do dado mais recente** | Periodicidade mensal. Dado mais recente disponível em 04/10/2026: **agosto/2026, variação mensal de −0,32%** (consulta ao SGS, série 433, em 04/10/2026). A série está disponível desde 01/01/1980, tem unidade "variação percentual mensal" e fonte IBGE, conforme os metadados do SGS. |
| **Dado pessoal? — se sim, granularidade e o que será agregado** | Não. O IPCA é uma série estatística agregada e não contém dados pessoais de indivíduos. |

O Banco Central informa, para suas séries do SGS relacionadas ao IPCA, periodicidade mensal e disponibilização por meio da interface JSON do BCData/SGS.

## Campo 5 — Papéis

| Integrante | Papel | O que fica sob sua responsabilidade |
|---|---|---|
| **Diego Lopes** | Integração de dados | Consultar o BACEN, implementar a coleta do IPCA, garantir que os dados estejam disponíveis para a API e manter o README com o comando de execução da API 1. |
| **Samuel Luiz** | Desenvolvimento da API 2 | Implementar os cálculos de variação de preço e IPCA acumulado (regra do Campo 3), o template de explicação e a integração opcional do LLM. |
| **Fernando Cleyber** | Produto e validação externa | Definir o caso de uso, construir a página de uso, organizar os testes com comerciantes, registrar cada contato em `evidencias.csv` e acompanhar a divulgação do produto. |

## Campo 6 — Cronograma

| Data | O que estará pronto |
|---|---|
| **04/10 (Marco 1, entrega remota)** | API 1 funcional, consultando o IPCA (série 433) no BACEN e retornando os dados em JSON de forma organizada, com README contendo o comando exato para executá-la e documentação básica do endpoint. Arquivos de `03-modelos` na raiz do repositório com os nomes oficiais. |
| **11/10** | Primeira rodada de contato com comerciantes registrada em `evidencias.csv`. |
| **25/10** | Segunda rodada de contato registrada. |
| **13/11 (Marco 2)** | API 2 funcional, com a regra de cálculo do Campo 3, comparação e explicação em linguagem simples (template; LLM opcional). Página de uso mínima funcionando. Log de requisições ativo. |
| **27/11 (Marco 3)** | Produto **publicado num endereço na internet**, testado com o público externo, com pelo menos três comerciantes contatados (tentativas e retornos registrados em `evidencias.csv`). |
| **04/12 (Socialização)** | Apresentação do projeto e demonstração do produto funcionando no endereço publicado. |

**Dependências externas.**

- Não há chave de acesso ao BACEN.
- O LLM, se usado, exige chave e tem custo; por isso é opcional e o produto funciona sem ele.
- A hospedagem depende da disponibilidade do plano gratuito do provedor escolhido.
- A validação externa depende da disponibilidade dos comerciantes e a divulgação depende dos canais estudantis. Caso não haja resposta, as tentativas e suas datas serão registradas e a equipe seguirá com testes internos.

## Campo 7 — Indicadores

| | Medida | Como será coletada | Valor que seria bom |
|---|---|---|---|
| **Contagem** | Número de chamadas à API 2 | Log de requisições da própria API (uma linha por chamada, com data e hora), exportado no Marco 3 | Mais de 20 chamadas |
| **Qualitativa** | Compreensão da comparação entre a variação do preço e o IPCA | Pergunta direta ao comerciante após o teste: "Você conseguiu entender se o preço aumentou acima, abaixo ou próximo da inflação?" | Pelo menos 2 respostas afirmativas. Se não houver respostas suficientes, vale o registro documentado de pelo menos 3 tentativas de contato. |

## Antes de entregar: a prova dos nove

- [ ] Riscamos tudo o que não conseguiríamos terminar até 13/11.
- [ ] O que sobrou ainda ajuda alguém.
- [ ] Uma pessoa de fora entende o Campo 1 e o Campo 3 sem explicação oral.
- [ ] A data da primeira conversa com o público está marcada: **até 11/10/2026**.
- [ ] Os indicadores podem ser coletados sem depender de terceiro (contagem: log da API; qualitativa: com alternativa documentada).
- [ ] Os arquivos estão na raiz do repositório com os nomes de `03-modelos`.
- [ ] Um clone limpo do repositório roda a API 1 seguindo só o README.

**Nota de escopo:** O projeto foi reduzido para concentrar-se em uma comparação objetiva entre a variação de preço de um produto e o IPCA acumulado entre dois meses. A API 1 será deliberadamente simples no Marco 1; cálculo, comparação, explicação e página de uso ficam para o Marco 2; publicação em endereço na internet e teste com o público ficam para o Marco 3.
