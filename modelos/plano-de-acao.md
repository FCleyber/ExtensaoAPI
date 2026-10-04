# Plano de ação

Rascunho em 11/09, versão final no Marco 1 (02/10).

---

## Identificação

* **Equipe:** Samuel Luiz [567412], Diego Lopes [556906], Fernando Cleyber [564872]
* **Trilha:** (A) API pública de dados abertos
* **Área temática da PREX:** Economia e cidadania 
* **Por que essa área, em uma linha:** Dados públicos de inflação podem ajudar pequenos comerciantes a compreender se os reajustes de preços acompanharam ou ficaram acima/abaixo da inflação do período.
* **Repositório:** https://github.com/FCleyber/ExtensaoAPI

## Campo 1 — O problema

Um pequeno comerciante que precisa reajustar o preço de um produto não consegue comparar de forma simples o aumento aplicado com a inflação acumulada no mesmo período.

## Campo 2 — O público externo

* **Quem é:** Pequenos comerciantes locais de Fortaleza que realizam reajustes de preços e têm interesse em compreender sua relação com a inflação, sem necessidade de conhecimento técnico em economia.
* **Duas ou três pessoas reais desse grupo:** Pelo menos três comerciantes locais que serão contatados pela equipe para testar e avaliar o produto.
* **Já falamos com alguma? Quando falaremos?** Ainda não. A primeira tentativa de contato está prevista para **18/10/2026** e uma segunda tentativa para **25/10/2026**. As tentativas e respectivas datas serão registradas no diário do projeto, independentemente de haver resposta.
* **Como essa pessoa vai descobrir que o produto existe:** Por meio de contato direto da equipe e, posteriormente, pela divulgação em canais de entidades estudantis e redes sociais relacionadas a negócios, economia e empreendedorismo.

## Campo 3 — Trilha e produto

* **O que é, em uma frase que caiba num tuíte, e onde ficará publicado:** Um serviço de APIs públicas que consulta o IPCA e permite comparar a variação do preço de um produto com a inflação acumulada em um período, apresentando o resultado em linguagem simples; ficará publicado no repositório público da equipe.

O produto será desenvolvido em duas etapas:

* **API 1:** consulta o IPCA disponibilizado pelo Banco Central e retorna os dados em JSON de forma organizada.

* **API 2:** recebe preço inicial, preço final e dois períodos, calcula a variação do preço e o IPCA acumulado, compara os resultados e utiliza um LLM apenas para explicar o resultado em linguagem simples.

* **O que NÃO faz parte:**

  * Determinar preço ideal para produtos.
  * Recomendar decisões financeiras ou comerciais individuais.
  * Prever preços futuros.
  * Estabelecer relação de causa e efeito entre inflação e o preço de um produto específico.
  * Fazer análise contábil ou financeira de empresas.
  * Utilizar dados da CVM, como DFP ou ITR.
  * Analisar décadas de histórico.
  * Explicar todas as causas da inflação.
  * Utilizar outros indicadores macroeconômicos inicialmente, caso não sejam necessários ao produto.
  * Substituir orientação econômica ou profissional.

## Campo 4 — Fontes de dados

|                                                                       |                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| :-------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Nome e órgão**                                                      | Sistema Gerenciador de Séries Temporais (SGS) — Banco Central do Brasil                                                                                                                                                                                                                                                                                                                                                                      |
| **Endereço**                                                          | `https://api.bcb.gov.br/dados/serie/bcdata.sgs.{código}/dados`                                                                                                                                                                                                                                                                                                                                                                               |
| **Licença — e o que ela permite ao nosso produto**                    | Os conjuntos de dados do IPCA disponibilizados no Portal de Dados Abertos do Banco Central estão sob a Open Data Commons Open Database License (ODbL). A licença permite utilizar, copiar, transformar e distribuir a base, observadas suas condições de atribuição e compartilhamento. O projeto identificará o Banco Central como fonte dos dados e observará os requisitos da licença caso dados ou bases derivadas sejam redistribuídos. |
| **Atualização — periodicidade declarada e data do dado mais recente** | Periodicidade mensal. A data do dado mais recente será registrada pela equipe no momento da implementação da API 1, considerando a última observação disponível na fonte utilizada.                                                                                                                                                                                                                                                          |
| **Dado pessoal? — se sim, granularidade e o que será agregado**       | Não. O IPCA é uma série estatística agregada e não contém dados pessoais de indivíduos.                                                                                                                                                                                                                                                                                                                                                      |

O Banco Central informa, para suas séries do SGS relacionadas ao IPCA, periodicidade mensal e disponibilização por meio da interface JSON do BCData/SGS.

## Campo 5 — Papéis

| **Integrante**       | **Papel**                   | **O que fica sob sua responsabilidade**                                                                                  |
| :------------------- | :-------------------------- | :----------------------------------------------------------------------------------------------------------------------- |
| **Diego Lopes**      | Integração de dados         | Consultar o BACEN, implementar a coleta do IPCA e garantir que os dados estejam disponíveis para a API.                  |
| **Samuel Luiz**      | Desenvolvimento da API 2    | Implementar os cálculos de variação de preço e IPCA acumulado e integrar o LLM para gerar a explicação.                  |
| **Fernando Cleyber** | Produto e validação externa | Definir o caso de uso, organizar os testes com comerciantes, registrar os contatos e acompanhar a divulgação do produto. |

## Campo 6 — Cronograma

| **Data**                 | **O que estará pronto**                                                                                                                                                     |
| :----------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **02/10 (Marco 1)**      | API 1 funcional, realizando uma consulta ao IPCA do BACEN e retornando os dados em JSON de forma organizada, com documentação básica do endpoint.                           |
| **13/11 (Marco 2)**      | API 2 funcional, recebendo preços e períodos, calculando a variação do preço e o IPCA acumulado e retornando uma comparação acompanhada de explicação em linguagem simples. |
| **27/11 (Marco 3)**      | Produto testado com o público externo, com pelo menos três tentativas documentadas de contato com comerciantes e registro dos retornos obtidos.                             |
| **04/12 (Socialização)** | Apresentação do projeto e demonstração das APIs funcionando.                                                                                                                |

**Dependências externas.** O projeto não depende de chave de acesso ao BACEN. A validação externa depende da disponibilidade dos comerciantes contatados e a divulgação depende da disponibilidade dos canais estudantis. Caso não haja resposta dos comerciantes, as tentativas de contato e suas datas serão registradas no diário e a equipe continuará os testes internos do produto.

## Campo 7 — Indicadores

|                 | **Medida**                                                   | **Como será coletada**                                                                                                               | **Valor que seria bom**                                         |
| :-------------- | :----------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------- |
| **Contagem**    | Número de chamadas realizadas à API 2                        | Registro das requisições realizadas durante os testes e demonstrações                                                                | Mais de 20 chamadas                                             |
| **Qualitativa** | Compreensão da comparação entre a variação do preço e o IPCA | Pergunta direta ao usuário externo após o teste: “Você conseguiu entender se o preço aumentou acima, abaixo ou próximo da inflação?” | Pelo menos 2 pessoas responderem que compreenderam a comparação |

## Antes de entregar: a prova dos nove

* [x] Riscamos tudo o que não conseguiríamos terminar até 13/11.
* [x] O que sobrou ainda ajuda alguém.
* [x] Uma pessoa de fora entende o Campo 1 e o Campo 3 sem explicação oral.
* [x] A data da primeira conversa com o público está marcada: **18/10/2026**.
* [x] Os indicadores podem ser coletados sem depender de terceiro.

---

**Nota de escopo:** O projeto foi reduzido para concentrar-se em uma comparação objetiva entre a variação de preço de um produto e o IPCA acumulado em dois períodos. A API 1 será deliberadamente simples no Marco 1; a parte de cálculo, comparação e explicação por LLM ficará para o Marco 2.
