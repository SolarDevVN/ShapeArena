import json

with open("data\coin.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(data)

data["tamgia"] = 1

with open("data\coin.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)