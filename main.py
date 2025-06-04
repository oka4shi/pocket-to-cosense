import json
import os
import requests

import jinja2


def get_from_pocket(consumer_key, access_token, limit=-1):
    """
    Fetches data from Pocket using the provided consumer key and access token.
    """
    COUNT = 30

    url = "https://getpocket.com/v3/get"
    headers = {
        "Host": "getpocket.com",
        "Content-Type": "application/json; charset=UTF-8",
    }

    result = []
    total = 1
    offset = 0
    while offset < total and (limit == -1 or offset < limit):
        count = min(COUNT, limit - offset) if limit > 0 else COUNT
        data = {
            "consumer_key": consumer_key,
            "access_token": access_token,
            "count": count,
            "offset": offset,
            "detailType": "complete",
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            print(f"Error fetching data from Pocket: {response.status_code}")
            return None

        resp_json = response.json()
        print(resp_json)

        total = resp_json.get("list", 0)
        for item in resp_json["list"]:
            result.append(resp_json["list"][item])

        offset += count

    return result


def main():
    consumer_key = os.getenv("POCKET_CONSUMER_KEY")
    access_token = os.getenv("POCKET_ACCESS_TOKEN")
    limit = int(os.getenv("LIMIT", -1))
    data = get_from_pocket(consumer_key, access_token, limit)
    if data is None:
        print("Failed to retrieve data from Pocket.")
        return

    with open("template.txt", "r") as f:
        template_str = f.read()

    template = jinja2.Template(template_str)

    output_json = {"pages": []}
    for item in data:
        rendered = template.render(**item)
        lines = rendered.splitlines()
        output_json["pages"].append(
            {
                "title": lines[0].strip(),
                "lines": lines,
            }
        )

    with open("output.json", "w") as f:
        f.write(json.dumps(output_json, indent=2))


if __name__ == "__main__":
    main()
