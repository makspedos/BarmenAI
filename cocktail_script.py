import requests
import json
import string

all_drinks = []

for letter in string.ascii_lowercase:
    url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={letter}"
    response = requests.get(url)
    data = response.json()
    drinks = data.get("drinks")
    if drinks:
        all_drinks.extend(drinks)

# Зберігаємо у файл
with open("all_cocktails.json", "w", encoding="utf-8") as f:
    json.dump(all_drinks, f, ensure_ascii=False, indent=2)