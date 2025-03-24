# coding:utf-8

from functools import wraps
import os
from typing import Any
from typing import Optional

from flask import Flask
from flask import Response
from flask import redirect  # noqa:H306
from flask import render_template_string
from flask import request
from flask import url_for
import requests
from xhtml import FlaskProxy
from xhtml import LocaleTemplate
from xkits import cmds

from xpw import AuthInit
from xpw import BasicAuth
from xpw import SessionPool

AUTH: BasicAuth
PROXY: FlaskProxy
SESSIONS: SessionPool
TEMPLATE: LocaleTemplate

BASE: str = os.path.dirname(__file__)
APP: Flask = Flask(__name__)
HOST: str = "0.0.0.0"
PORT: int = 3000


def run():
    APP.secret_key = SESSIONS.secret.key
    APP.run(host=HOST, port=PORT)


def auth() -> Optional[Any]:
    cmds.logger.debug("request.headers:\n%s", request.headers)
    host: Optional[str] = request.headers.get("Host")
    if host == f"localhost:{PORT}":
        cmds.logger.debug("Skip python-requests.")
        return None
    session_id: Optional[str] = request.cookies.get("session_id")
    if session_id is None:
        response = redirect(url_for("proxy", path=request.path.lstrip("/")))
        response.set_cookie("session_id", SESSIONS.search().name)
        return response
    cmds.logger.debug("%s request verify.", session_id)
    if SESSIONS.verify(session_id):
        # cmds.logger.info("%s is logged.", session_id)
        return None  # logged
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not password:  # invalid password
            cmds.logger.info("%s login to %s with empty password.", session_id, username)  # noqa:E501
        elif AUTH.verify(username, password):
            SESSIONS.sign_in(session_id)
            cmds.logger.info("%s sign in with %s.", session_id, username)
            return redirect(url_for("proxy", path=request.path.lstrip("/")))
        cmds.logger.warning("%s login to %s error.", session_id, username)
    cmds.logger.debug("%s need to login.", session_id)
    context = TEMPLATE.search(request.headers.get("Accept-Language", "en"), "login").fill()  # noqa:E501
    return render_template_string(TEMPLATE.seek("login.html").loads(), **context)  # noqa:E501


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (response := auth()) is not None:
            return response
        return f(*args, **kwargs)
    return decorated_function


@APP.route("/favicon.ico", methods=["GET"])
def favicon() -> Response:
    if (response := PROXY.request(request)).status_code == 200:
        return response
    session_id: Optional[str] = request.cookies.get("session_id")
    logged: bool = isinstance(session_id, str) and SESSIONS.verify(session_id)
    binary: bytes = TEMPLATE.seek("unlock.ico" if logged else "locked.ico").loadb()  # noqa:E501
    return APP.response_class(binary, mimetype="image/vnd.microsoft.icon")


@APP.route("/", defaults={"path": ""}, methods=["GET", "POST"])
@APP.route("/<path:path>", methods=["GET", "POST"])
@login_required
def proxy(path: str) -> Response:  # pylint: disable=unused-argument
    try:
        response: Response = PROXY.request(request)
        cmds.logger.debug("response.headers:\n%s", response.headers)
        return response
    except requests.ConnectionError:
        return Response("Bad Gateway", status=502)


if __name__ == "__main__":
    AUTH = AuthInit.from_file()
    PROXY = FlaskProxy("http://127.0.0.1:8000")
    TEMPLATE = LocaleTemplate(os.path.join(BASE, "resources"))
    SESSIONS = SessionPool(lifetime=86400)  # 1 day
    run()
