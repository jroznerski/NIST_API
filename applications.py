import requests
import csv

device_uuid = "***"
api_url = "https://"

headers = {
    "Accept": "application/json",
    "Authorization": "Basic==",
    "aw-tenant-code": "="
}

try:
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        app_items = data.get("app_items", [])

        with open("aplikacje.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "Nazwa aplikacji",
                "Status przypisania",
                "Wersja przypisana",
                "Status zainstalowania",
                "Zainstalowana wersja",
                "Ostatnia akcja UEM",
                "Czas ostatniej akcji UEM",
                "Bundle ID"
            ])

            for app in app_items:
                name = app.get("name", "")
                assignment_status = app.get("assignment_status", "")
                assigned_version = app.get("assigned_version", "")
                installed_status = app.get("installed_status", "")
                installed_version = app.get("installed_version", "")
                latest_uem_action = app.get("latest_uem_action", "")
                latest_uem_action_time = app.get("latest_uem_action_time", "")
                bundle_id = app.get("bundle_id", "")

                writer.writerow([
                    name,
                    assignment_status,
                    assigned_version,
                    installed_status,
                    installed_version,
                    latest_uem_action,
                    latest_uem_action_time,
                    bundle_id
                ])

        print("Dane zapisano do pliku aplikacje.csv")
    else:
        print("Błąd zapytania HTTP. Kod odpowiedzi:", response.status_code)

except Exception as e:
    print("Błąd:", e)
