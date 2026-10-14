"""Schema da saida estruturada do LLM — escopo do plano de 04/10.

O LLM nunca calcula (Campo 3 do plano). Ele so recebe numeros ja prontos
e devolve uma frase em linguagem simples."""
from __future__ import annotations
from pydantic import BaseModel, Field


class ExplicacaoReajuste(BaseModel):
    explicacao: str = Field(
        description=(
            "1 a 2 frases, em linguagem simples, explicando se o reajuste "
            "ficou acima, abaixo ou proximo do IPCA acumulado no periodo. "
            "Deve usar exatamente os numeros fornecidos, sem inventar nem "
            "arredondar de forma diferente do que foi passado."
        )
    )