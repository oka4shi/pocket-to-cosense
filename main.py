import json
import os
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

import jinja2


def request_url(url, headers=None, data=None):
    req = urllib.request.Request(url, json.dumps(data).encode(), headers)
    try:
        with urllib.request.urlopen(req) as res:
            response_str = res.read().decode("utf-8")
            headers = res.getheaders()
            response = json.loads(response_str)
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} {e.reason}")
        print(f"Response: {e.headers}")
        raise e

    return response


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = "Oauth authorization complete. Close this window and return to the terminal."


        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()

        # ボディを送信
        self.wfile.write(data.encode('utf-8'))

def get_access_token(consumer_key, redirect_uri):
    """
    Retrieves the access token for Pocket using the provided consumer key.
    """
    url = "https://getpocket.com/v3/oauth/request"
    headers = {
        "Host": "getpocket.com",
        "Content-Type": "application/json; charset=UTF-8",
        "X-Accept": "application/json",
    }
    data = {
        "consumer_key": consumer_key,
        "redirect_uri": redirect_uri,
    }
    response = request_url(url, headers=headers, data=data)
    code = response.get("code")

    print("Please visit the following URL to authorize the application:")
    print(f"https://getpocket.com/auth/authorize?request_token={code}&redirect_uri={redirect_uri}")
    server = HTTPServer(("0.0.0.0", 8080), HTTPRequestHandler)
    server.handle_request()

    url = "https://getpocket.com/v3/oauth/authorize"
    headers = {
        "Host": "getpocket.com",
        "Content-Type": "application/json; charset=UTF-8",
        "X-Accept": "application/json",
    }
    data = {
        "consumer_key": consumer_key,
        "code": code
    }
    response = request_url(url, headers=headers, data=data)

    return response.get("access_token")


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

    titles = []
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

        response = request_url(url, headers=headers, data=data)

        total = response.get("total", 0)

        print(f"{offset + len(response['list'])} / {total}")
        for id in response["list"]:
            item = response["list"][id]
            if item.get("status", 2) == 2:
                print(f"skipped: {item}")
                continue

            fields = {
                    "title": item.get("given_title") or item.get("resolved_title"),
                    "url": item.get("given_url") or item.get("resolved_url"),
                    }
            if not fields["title"]:
                if fields["url"]:
                    fields["title"] = fields["url"]
                else:
                    print(f"skipped: {item}")
                    continue

            i = 2
            while fields["title"] in titles:
                fields["title"] += f" {i}"
                i += 1

            titles.append(fields["title"])
            result.append(fields | item)

        offset += count

    return result

def main():
    consumer_key = os.getenv("POCKET_CONSUMER_KEY")
    redirect_uri = os.getenv("POCKET_REDIRECT_URI", "http://localhost:8080")
    access_token = get_access_token(consumer_key, redirect_uri)
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

    with open("output/output.json", "w") as f:
        f.write(json.dumps(output_json, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
