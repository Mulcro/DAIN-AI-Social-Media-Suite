from flask import Flask, request, redirect, make_response
import random
import string
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY")
REDIRECT_URI = os.getenv("TIKTOK_REDIRECT_URI")

@app.route('/oauth')
def oauth():
    csrf_state = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    res = make_response()
    res.set_cookie('csrfState', csrf_state, max_age=60)

    params = {
        "client_key": CLIENT_KEY,
        "scope": "user.info.basic,video.upload",
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "state": csrf_state
    }

    auth_url = "https://www.tiktok.com/v2/auth/authorize/?" + urllib.parse.urlencode(params)

    res.headers['Location'] = auth_url
    res.status_code = 302
    return res

if __name__ == '__main__':
    app.run(debug=True)
