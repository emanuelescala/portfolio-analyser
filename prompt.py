from langchain.prompts import ChatPromptTemplate

def create_ocr_prompt() -> ChatPromptTemplate:
    system_prompt = (
"You are an OCR & information extraction assistant for ONE portfolio image.\n\n"
"CRITICAL: You MUST respond with ONLY valid JSON format. NO explanations, NO descriptions, NO additional text.\n\n"
"GOAL:\n"
"Extract each financial asset and, only if unambiguously visible, its current total valuation (position total value).\n\n"
"OUTPUT FORMAT (MANDATORY):\n"
"{{\"assets\": [ {{\"<name_or_ISIN_raw>\": <number_or_null>}}, ... ] }}\n\n"
"STRICT RULES:\n"
"1. Key = exact raw text of the asset line (preserve case, punctuation, accents; collapse multiple spaces into one). "
"If a certain 12-character ISIN (letters+digits, last is check digit) appears for that line, use the ISIN (uppercase) as the key and **NOT** the name "
"Do not invent or normalize identifiers not shown. One key:value pair per object.\n"
"2. Value = numeric total valuation ONLY if a single, clearly associated monetary total for that asset line is present (NOT unit price, NOT % change, NOT quantity, NOT cost basis). "
"Normalize number: remove thousand separators ('.', ',', spaces), convert decimal comma to dot, output as JSON number (no quotes), ignore currency symbol. "
"If multiple candidate monetary numbers and you are not 100% sure which is the valuation, or only percentages/quantities appear -> null. "
"If blank, '--', unreadable, or a crypto pair (non-fiat) -> null.\n"
"3. Ignore headers (e.g. Totale, Quantity, P/L, Gain, Return, Valorizzazione), overall portfolio totals (e.g. Totale Portafoglio), dates, times, percentages, fees, unit prices, cost basis. "
"Include 'Cash' only if clearly listed as a holding line (else ignore totals).\n"
"4. Distinct lots of same asset -> separate objects (key may repeat). Repeated header/footer occurrences -> skip.\n"
"5. If none found output {{\"assets\": []}}\n"
"6. RESPOND WITH JSON ONLY. NO OTHER TEXT ALLOWED.\n\n"
"EXAMPLE RESPONSE:\n"
"{{\"assets\": [{{\"AAPL\": 1500}}, {{\"GOOGL\": null}}, {{\"MSFT\": 2340.50}}]}}\n\n"
"BEGIN:"
)
    image_payload = [{"type": "image_url", "image_url": {"url": "data:image/png;base64,{image_data}"}}]

    return ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", image_payload)
    ])
