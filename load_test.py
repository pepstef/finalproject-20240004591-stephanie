import json, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

API_URL = "https://47be8is7ma.execute-api.ap-southeast-2.amazonaws.com/prod"
API_KEY = "D1bPeFY0GWabZzU7LHZq80nAwCd6ywj8UxbryKw8"

def create_parcel(i):
    start = time.time()
    try:
        body = json.dumps({
            "sender": f"Driver-{i}",
            "receiver": f"Customer-{i}",
            "address": f"Addr-{i}",
            "email": f"c{i}@example.com"
        }).encode()

        req = urllib.request.Request(
            f"{API_URL}/parcels",
            data=body,
            headers={
                "Content-Type": "application/json",
                "x-api-key": API_KEY,
                "X-User-Role": "driver"
            },
            method="POST"
        )

        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())

        return {
            "id": i,
            "success": True,
            "parcel_id": data.get("parcel_id", ""),
            "time": round(time.time() - start, 3)
        }

    except Exception as e:
        return {
            "id": i,
            "success": False,
            "error": str(e),
            "time": round(time.time() - start, 3)
        }

def main():
    num = 20
    print(f"SmartParcel API Load Test — {num} concurrent requests")

    start = time.time()

    with ThreadPoolExecutor(max_workers=num) as pool:
        results = list(pool.map(create_parcel, range(1, num + 1)))

    total = round(time.time() - start, 3)

    for r in results:
        print(f"  {r['id']}: {'OK' if r['success'] else 'FAIL'} {r.get('parcel_id','')} {r['time']}s")

    ok = sum(1 for r in results if r['success'])

    print(f"Results: {ok}/{num}, total: {total}s")

if __name__ == "__main__":
    main()
