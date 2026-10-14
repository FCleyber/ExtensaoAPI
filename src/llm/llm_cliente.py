"""
explicação da API 2 — escopo do plano de 04/10 (Campo 3).

O LLM nunca calcula: a variação de preço e o IPCA acumulado já vêm
prontos do código (ver regra de cálculo no plano de ação). Esta camada
só decide COMO dizer isso em linguagem simples.

"""
from __future__ import annotations
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from schemas import ExplicacaoReajuste

PROMPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts")
MAX_OUTPUT_TOKENS = 500


def _ler_prompt(nome: str) -> str:
    with open(os.path.join(PROMPT_DIR, nome), encoding="utf-8") as f:
        return f.read()


def template_determinístico(classificacao: str, diferenca_pp: float,
                            variacao_preco_pct: float, ipca_acumulado_pct: float) -> str:
    """Explicação padrão, sem LLM. Sempre disponível, sempre a mesma lógica."""
    diferenca_abs = abs(round(diferenca_pp, 1))
    if classificacao == "acima":
        return (
            f"O reajuste de {variacao_preco_pct:.1f}% ficou acima da inflação "
            f"do período ({ipca_acumulado_pct:.1f}%), uma diferença de "
            f"{diferenca_abs} pontos percentuais.")
    if classificacao == "abaixo":
        return (
            f"O reajuste de {variacao_preco_pct:.1f}% ficou abaixo da inflação "
            f"do período ({ipca_acumulado_pct:.1f}%), uma diferença de "
            f"{diferenca_abs} pontos percentuais.")
    return (
        f"O reajuste de {variacao_preco_pct:.1f}% ficou próximo da inflação "
        f"do período ({ipca_acumulado_pct:.1f}%), com diferença de apenas "
        f"{diferenca_abs} ponto(s) percentual(is).")


def _provedor_disponivel() -> str | None:
    if os.getenv("ANTHROPIC_API_KEY"):
        return "anthropic"
    if os.getenv("GEMINI_API_KEY"):
        return "gemini"
    return None


def _call_anthropic(system: str, user: str) -> ExplicacaoReajuste:
    import anthropic
    client = anthropic.Anthropic()
    tool = {
        "name": "responder",
        "description": "Retorna a explicação no formato estruturado exigido.",
        "input_schema": ExplicacaoReajuste.model_json_schema(),
    }
    resp = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
        max_tokens=MAX_OUTPUT_TOKENS,
        system=system,
        tools=[tool],
        tool_choice={"type": "tool", "name": "responder"},
        messages=[{"role": "user", "content": user}],
    )
    for block in resp.content:
        if block.type == "tool_use":
            return ExplicacaoReajuste.model_validate(block.input)
    raise RuntimeError("Anthropic não retornou tool_use.")


def _call_gemini(system: str, user: str) -> ExplicacaoReajuste:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    schema = ExplicacaoReajuste.model_json_schema()
    schema.pop("$defs", None)

    resp = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=user,
        config=types.GenerateContentConfig(
            system_instruction=system,
            temperature=0,
            response_mime_type="application/json",
            response_schema=schema,
            max_output_tokens=MAX_OUTPUT_TOKENS,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        ),
    )
    return ExplicacaoReajuste.model_validate(json.loads(resp.text))


def explicar_reajuste(variacao_preco_pct: float, ipca_acumulado_pct: float,
                      classificacao: str, mes_inicial: str, mes_final: str) -> str:
    """Interface pública usada pela API 2.

    Todos os números já vêm calculados pelo código (regra do plano,
    Campo 3). Esta função só decide a frase final — nunca um valor."""
    diferenca_pp = variacao_preco_pct - ipca_acumulado_pct
    texto_padrao = template_determinístico(
        classificacao, diferenca_pp, variacao_preco_pct, ipca_acumulado_pct)

    usar_llm = os.getenv("USAR_LLM_EXPLICACAO") == "1"
    provedor = _provedor_disponivel()
    if not usar_llm or not provedor:
        return texto_padrao

    system = _ler_prompt("explicar_reajuste.txt")
    user = (
        f"Período: {mes_inicial} a {mes_final}\n"
        f"Variação do preço: {variacao_preco_pct:.2f}%\n"
        f"IPCA acumulado no período: {ipca_acumulado_pct:.2f}%\n"
        f"Classificação (já decidida pelo código): {classificacao}\n"
        f"Diferença: {diferenca_pp:.2f} pontos percentuais")

    try:
        if provedor == "anthropic":
            return _call_anthropic(system, user).explicacao
        return _call_gemini(system, user).explicacao
    except Exception:
        # Qualquer falha do LLM cai pro template — a API 2 nunca quebra por isso.
        return texto_padrao