# gogov
Unofficial API Client for GoGov CRM

## install
```sh
pip install gogov
```

## basic CLI usage
```sh
gogov export-requests --email="jdoe@fakecity.gov" --password="2c56477e97ab8b2d180a6513" --site="fakecityXYZ" --city-id="123" $PWD/requests.csv
```

## basic Python usage
```python
from gogov import Client

# client automatically logs in when initialized
client = Client(
    username = "jdoe",
    password = "2c56477e97ab8b2d180a6513",
    site = "fakecityXYZ",
    city_id = "123"
)

## download csv of all requests to a file
client.export_requests("requests.csv")

## log out
client.logout()
```

## advanced usage
coming soon