import os, requests


def token(request):
    if not "Authorization" in request.headers:
        return None, ("Missing credentials", 401)

    token = request.headers["Authorization"]

    if not token:
        return None, ("Missing credentials", 401)

    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "Authorization": token,
    }
    response = requests.post(
        f"http://{os.environ.get('AUTH_SERVICE_ADDRESS')}/validate",
        headers=headers,
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
