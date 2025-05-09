import requests

def get_latest_data():
    url = "https://taixiu1.gsum01.com/api/luckydice1/GetSoiCau"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    print("[INFO] Đang lấy dữ liệu từ API...")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"[INFO] Lấy được {len(data)} dòng dữ liệu.")
        return data
    except Exception as e:
        print(f"[LỖI] Không thể lấy dữ liệu từ API: {e}")
        return None

def parse_results(data):
    print("[INFO] Đang phân tích kết quả...")
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
    print(f"[INFO] Phân tích xong, có {len(results)} kết quả.")
    return results

def predict_next(results):
    print("[INFO] Đang dự đoán kết quả tiếp theo...")
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

def main():
    print("[INFO] Bắt đầu script tài/xỉu...")
    data = get_latest_data()
    if not data:
        print("[THÔNG BÁO] Không có dữ liệu từ API.")
        return

    data.reverse()
    results = parse_results(data)
    if not results:
        print("[THÔNG BÁO] Không có kết quả hợp lệ sau khi xử lý.")
        return

    current = results[-1]
    prediction = predict_next(results)
    print(f"[KẾT QUẢ] Kết quả mới: {current} | Dự đoán tiếp theo: {prediction}")

if __name__ == "__main__":
    main()
