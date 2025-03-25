import argparse
import csv
from collections import OrderedDict
import json
import requests
from time import sleep, time

import flatmate


class Client:
    def __init__(self, email, password, site, city_id, wait=10):
        if wait is None:
            wait = 10
        self.base = "https://api.govoutreach.com"
        self.site = site
        self.city_id = city_id
        self.wait = wait
        self.prevtime = None
        self.login(email, password)

    def throttle(self):
        current = time()
        if isinstance(self.prevtime, float):
            wait_time = self.prevtime + self.wait - current
            if wait_time > 0:
                print("[gogov] sleeping " + str(wait_time) + " seconds")
                sleep(wait_time)
        self.prevtime = current

    def login(self, email, password):
        url = self.base + "/users/sessions"
        headers = {"Content-Type": "application/json", "X-Gogovapps-Site": self.site}
        self.throttle()
        r = requests.post(
            url, headers=headers, json={"email": email, "password": password}
        )
        data = r.json()
        self.token = data["token"]
        self.access_token = data["access_token"]
        self.refresh_token = data["refresh_token"]
        self.expiry = data["expiry"]
        self.session_id = data["id"]
        return data

    def logout(self):
        print("[gogov] logging out")
        url = self.base + "/users/sessions"
        headers = {
            "Authorization": self.token,
            "Content-Type": "application/json",
            "X-Gogovapps-Site": self.site,
        }
        self.throttle()
        r = requests.delete(url, headers=headers)
        data = r.json()
        print("[gogov] logged out")

    def get_all_topic_info(self):
        url = self.base + "/crm/requests/all_topic_info"
        headers = {
            "Authorization": self.token,
            "Content-Type": "application/json",
            "X-Gogovapps-Site": self.site,
        }
        self.throttle()
        r = requests.get(url, headers=headers)
        data = r.json()
        return data

    def get_topics(self):
        url = self.base + "/core/crm/topics"
        headers = {
            "Authorization": self.token,
            "Content-Type": "application/json",
            "X-Gogovapps-Site": self.site,
        }
        self.throttle()
        r = requests.get(url, headers=headers)
        data = r.json()
        return data

    def search(self):
        url = self.base + "/core/crm/search"
        headers = {"Authorization": self.token, "X-Gogovapps-Site": self.site}

        searchAfter = []

        results = []

        for i in range(1_000_000):
            payload = {
                "cityId": self.city_id,
                "searchAfter": searchAfter,
                "size": 100,
                "sort": [
                    {"dateEntered": {"missing": "_last", "order": "desc"}},
                    {"_id": "desc"},
                ],
            }
            print("[gogov] url:", url)
            # print("[gogov] headers:", headers)
            print("[gogov] payload:", payload)
            self.throttle()
            r = requests.post(url, headers=headers, json=payload)
            self.prevtime = (
                time()
            )  # throttle based on time the request completed (not started)
            print(
                "[gogov] response:", r.text[:500], ("..." if len(r.text) > 1000 else "")
            )
            data = r.json()

            hits = data["hits"]["hits"]

            if len(hits) == 0:
                break

            searchAfter = hits[-1]["sort"]

            sources = [hit["_source"] for hit in hits]

            results += sources

        return results

    def export_requests(self, filepath=None, fh=None, custom_fields=None):
        # all_topic_info = self.get_all_topic_info()

        # get list of all topic ids
        # all_topic_ids = [t['id'] for t in all_topic_info]

        base_columns = OrderedDict(
            [
                ("caseId", "caseId"),
                ("caseType", "caseType"),
                ("classificationType", "classificationId"),
                ("departmentId", "departmentId"),
                ("contactId", "contactId"),
                ("contact2Id", "contact2Id"),
                ("description", "description"),
                ("location", "location"),
                ("latitude", "locationPoint.lat"),
                ("longitude", "locationPoint.lon"),
                ("dateEntered", "dateEntered"),
                ("howEntered", "howEntered"),
                ("enteredById", "enteredById"),
                ("status", "status"),
                ("assignedToId", "assignedToId"),
                ("dateClosed", "dateClosed"),
                ("closedById", "closedById"),
                ("reasonClosed", "reasonClosed"),
                ("dateExpectClose", "dateExpectClose"),
                ("priority", "priority"),
                ("cecaseId", "cecaseId"),
                ("dateLastUpdated", "dateLastUpdated"),
                ("contact.firstName", "contact.firstName"),
                ("contact.lastName", "contact.lastName"),
                ("contact.phone", "contact.phone"),
            ]
        )

        custom_columns = OrderedDict([])

        all_results = []
        for page in range(1):
            results = self.search()

            for source in results:
                # overwrite custom fields, converting from list of dictionaries to a simple dictionary
                source["customFields"] = dict(
                    [
                        (fld["name"], fld["value"])
                        for fld in source["customFields"]
                        if fld.get("name")
                    ]
                )

                # add to custom fields
                if custom_fields is None:
                    for name in source["customFields"].keys():
                        if "." not in name:
                            if name not in custom_columns:
                                custom_columns[name] = ".".join(["customFields", name])

                # just want the source part
                all_results.append(source)

        if custom_fields is not None:
            custom_columns = OrderedDict(
                [(fld, ".".join(["customFields", fld])) for fld in custom_fields]
            )

        columns = OrderedDict(list(base_columns.items()) + list(custom_columns.items()))

        print("[gogov] columns:", columns)
        flattened_results = flatmate.flatten(
            all_results, columns=columns, clean=True, skip_empty_columns=False
        )

        f = fh or open(filepath, "w", newline="", encoding="utf-8")

        writer = csv.DictWriter(f, fieldnames=list(columns.keys()))
        writer.writeheader()
        writer.writerows(flattened_results)

        if fh is None:
            f.close()


def main():
    parser = argparse.ArgumentParser(
        prog="gogov",
        description="High-Level API Client for GoGov",
    )
    parser.add_argument(
        "method",
        help='method to run, can be "export-requests"',
    )
    parser.add_argument(
        "outpath", help="output filepath of where to save downloaded CSV"
    )
    parser.add_argument(
        "--base",
        type=str,
        help='base url for the API, like "https://api.govoutreach.com"',
    )
    parser.add_argument("--city-id", type=str, help="city id")
    parser.add_argument(
        "--custom-fields",
        type=str,
        help="comma-separated list of custom fields to include",
    )
    parser.add_argument("--email", type=str, help="email")
    parser.add_argument("--password", type=str, help="password")
    parser.add_argument("--site", type=str, help="site")
    parser.add_argument("--wait", type=float, help="wait")
    args = parser.parse_args()

    if args.method not in ["export-requests", "export_requests"]:
        raise Except("[gogov] invalid or missing method")

    client = Client(
        email=args.email,
        password=args.password,
        site=args.site,
        city_id=args.city_id,
        wait=args.wait,
    )

    if args.method in ["export-requests", "export_requests"]:
        custom_fields = args.custom_fields.split(",") if args.custom_fields else None
        client.export_requests(args.outpath, custom_fields=custom_fields)

    client.logout()


if __name__ == "__main__":
    main()
