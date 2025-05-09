import requests
import time

def get_latest_data():
    url = "https://taixiu1.gsum01.com/api/luckydice1/GetSoiCau"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except:
        return None

def parse_results(data):
    results = []
    for item in data:
        x1, x2, x3 = item.get("FirstDice"), item.get("SecondDice"), item.get("ThirdDice")
        if None in (x1, x2, x3):
            continue
        total = x1 + x2 + x3
        if 11 <= total <= 17:
            results.append("Tài")
        elif 4 <= total <= 10:
            results.append("Xỉu")
    return results

def predict_next(results):
    if len(results) < 3:
        return "Không đủ dữ liệu"
    last3 = results[-3:]
    if last3 == ["Tài", "Xỉu", "Tài"]:
        return "Xỉu"
    elif last3 == ["Xỉu", "Tài", "Xỉu"]:
        return "Tài"
    else:
        tai_count = results[-10:].count("Tài")
        xiu_count = results[-10:].count("Xỉu")
        return "Tài" if tai_count > xiu_count else "Xỉu"

def main_loop(interval=5):
    last_result = None

    while True:
        data = get_latest_data()
        if not data:
            time.sleep(interval)
            continue

        data.reverse()
        results = parse_results(data)
        if not results:
            time.sleep(interval)
            continue

        current = results[-1]
        if current != last_result:
            print(f"Kết quả mới: {current} | Dự đoán tiếp theo: {predict_next(results)}")
            last_result = current

        time.sleep(interval)

if __name__ == "__main__":
    main_loop()
