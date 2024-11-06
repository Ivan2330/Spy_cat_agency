import httpx
from typing import List
from fastapi import HTTPException

# URL для отримання порід котів з TheCatAPI
API_URL = "https://api.thecatapi.com/v1/breeds"

async def fetch_breeds() -> List[str]:
    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL)
        response.raise_for_status()
        breeds_data = response.json()
        # Повертає список назв порід
        return [breed["name"] for breed in breeds_data]

# Функція для валідації породи
async def validate_breed(breed: str) -> None:
    breeds = await fetch_breeds()
    # Якщо порода не знайдена в списку, піднімаємо виняток
    if breed not in breeds:
        raise HTTPException(status_code=400, detail="Invalid breed name.")
