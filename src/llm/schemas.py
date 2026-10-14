from __future__ import annotations
from pydantic import BaseModel, Field


class IndicadorCitado(BaseModel):
    serie: str = Field(description="Nome curto do indicador, ex.: 'ipca', 'selic'")
    valor: str = Field(description="Valor ou variação citada na narrativa, já formatado")
    papel: str = Field(description="O que esse indicador explica no fenômeno descrito")


class NarrativaMacro(BaseModel):
    resumo: str = Field(description="Narrativa em linguagem simples, 1 a 3 paragrafos")
    titulo: str = Field(description="Titulo curto e direto para a narrativa")
    indicadores_usados: list[IndicadorCitado]
    fenomeno_principal: str = Field(
        description="Em uma frase: qual fenomeno macroeconomico esta sendo explicado")
    nivel_confianca: str = Field(
        description="'alto', 'medio' ou 'baixo' — baseado na qualidade/cobertura dos dados")


class ComparacaoPeriodos(BaseModel):
    periodo_atual: str
    periodo_anterior: str
    principais_mudancas: list[str] = Field(
        description="Lista curta das mudancas mais relevantes entre os periodos")
    narrativa: str = Field(description="Texto comparativo em linguagem simples")
    piorou_ou_melhorou: str = Field(
        description="Avaliacao geral: 'melhorou', 'piorou', 'estavel' ou 'misto'")