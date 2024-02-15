import re
from typing import List

import httpx
from telegram import Update
from telegram.ext import ContextTypes

import answers
from logger import logger
from settings import settings


async def convert(value: float, base: str, targets: List[str]) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            settings.EXCHANGE_RATE_URL.unicode_string(),
            params={
                "base_currency": base,
                "currencies": ",".join(targets),
            },
            headers={
                "apikey": settings.EXCHANGE_RATE_API_KEY,
            },
        )
        result = response.json()

    answer = ""
    for currency in result["data"].values():
        answer += f'{base} to {currency["code"]} - курс {currency["value"]:.3f} - итог {(value * currency["value"]):.3f}\n'

    return answer


async def unknown(input_text: str) -> str:
    if re.search(
        r"(привет|здравствуйте|приветствую|хай|здравствуй)", input_text, re.IGNORECASE
    ):
        return answers.GREETINGS_ANSWER

    if re.search(
        r"(до свидания|прощайте|пока|до встречи|всего хорошего)",
        input_text,
        re.IGNORECASE,
    ):
        return answers.GOODBYE_ANSWER
    
    return answers.UNKNOWN_ANSWER
