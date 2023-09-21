import requests
import json
from datetime import datetime, timedelta

current_datetime = datetime.now()

start_date = current_datetime - timedelta(days=7)
start_date = start_date.replace(hour=9, minute=0, second=0, microsecond=0)

end_date = current_datetime
end_date = end_date.replace(hour=9, minute=0, second=0, microsecond=0)

start_date_iso = start_date.isoformat()
end_date_iso = end_date.isoformat()

uri = f"https://services.nvd.nist.gov/rest/json/cves/2.0/"
if start_date_iso and end_date_iso:
    uri += f"?pubStartDate={start_date_iso}&pubEndDate={end_date_iso}"

response = requests.get(uri)

if response.status_code == 200:
    dane = response.json()
    print(dane)

    with open('dane.json', 'w', encoding='utf-8') as json_file:
        json.dump(dane, json_file, ensure_ascii=False, indent=4)
        print("Dane zostały zapisane do pliku 'dane.json'")
else:
    print(f"Żądanie nie powiodło się. Kod odpowiedzi: {response.status_code}")
