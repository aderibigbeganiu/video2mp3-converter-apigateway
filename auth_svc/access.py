import os
import requests
from dotenv import load_dotenv

load_dotenv()


def login(request):
    auth = request.authorization
    if not auth:
        return None, ("Missing credentials", 401)
    basicAuth = auth.username, auth.password

    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
    }

    response = requests.post(
        f'{os.environ.get("AUTH_SVC_ADDRESS")}/login',
        auth=basicAuth,
        verify=False,
        headers=headers,
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
