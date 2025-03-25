from __future__ import annotations

import logging
from functools import wraps
from typing import cast

from flask import Blueprint, request, jsonify, Response
from flask.views import MethodView

import ckan.types as types
from ckan.lib import helpers
from ckan.plugins import toolkit as tk, plugin_loaded
from ckan.logic import parse_params

from ckanext.auth import utils
from ckanext.auth.model import UserSecret

log = logging.getLogger(__name__)
auth = Blueprint("auth", __name__, url_prefix="/mfa")


def require_login(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if tk.current_user.is_anonymous:
            return tk.abort(401, tk._("You have to be logged in to access this page."))
        return func(*args, **kwargs)

    return decorated_view


class Configure2FA(MethodView):
    @require_login
    def get(self, user_id: str):
        try:
            user_dict = tk.get_action("user_show")(self.get_context(), {"id:": user_id})
        except tk.ObjectNotFound:
            tk.abort(404, tk._("User not found"))
        except tk.NotAuthorized:
            tk.abort(403, tk._("Not authorized to see this page"))

        extra_vars = {
            "user_id": user_id,
            "is_sysadmin": user_dict["sysadmin"],
            "is_myself": user_dict["name"] == tk.current_user.name,
            "user_dict": user_dict,
        }

        extra_vars.update(self._setup_totp_extra_vars(user_id))

        return tk.render(
            "auth/configure_2fa.html",
            extra_vars,
        )

    def get_context(self) -> types.Context:
        return {
            "user": tk.current_user.name,
            "auth_user_obj": tk.current_user,
        }

    @require_login
    def post(self, user_id: str):
        extra_vars = self._setup_totp_extra_vars(user_id)

        if extra_vars.get("code_valid"):
            tk.h.flash_success(
                tk._(
                    """
                    The code is valid. Your authenticator app is
                    now properly set up for future use."""
                )
            )
        else:
            tk.h.flash_error(
                tk._(
                    """The code is incorrect. Please try scanning
                the QR code with your authenticator app again."""
                )
            )

        return tk.redirect_to("auth.configure_2fa", user_id=user_id)

    def _setup_totp_extra_vars(self, user_id: str):
        data_dict = parse_params(tk.request.form)

        user_secret = UserSecret.get_for_user(user_id)

        if not user_secret:
            return {}

        test_code = cast(str, data_dict.get("code"))

        extra_vars = {
            "totp_secret": user_secret.secret,
            "provisioning_uri": user_secret.provisioning_uri,
        }

        if request.method == "POST" and test_code:
            extra_vars["code_valid"] = user_secret.check_code(
                test_code, verify_only=True
            )

        return extra_vars


@auth.route("/configure_mfa/<user_id>/new", methods=["GET", "POST"])
@require_login
def regenerate_secret(user_id: str):
    utils.regenerate_user_secret(user_id)
    tk.h.flash_success(tk._("Your 2FA secret has been regenerated."))
    return helpers.redirect_to("auth.configure_2fa", user_id=user_id)


@auth.route("/send_verification_code", methods=["POST"])
def send_verification_code() -> Response:
    user_name: str = tk.get_or_bust(dict(tk.request.form), "login")

    utils.regenerate_user_secret(user_name)
    success = utils.send_verification_email_to_user(user_name)

    return jsonify(
        {
            "success": success,
            "error": "Failed to send verification code" if not success else None,
            "result": None,
        }
    )


@auth.route("/init_qr_code", methods=["POST"])
def init_qr_code() -> Response:
    user_name: str = tk.get_or_bust(dict(tk.request.form), "login")

    secret = UserSecret.get_for_user(user_name)

    if not secret:
        secret = UserSecret.create_for_user(user_name)

    return jsonify(
        {
            "success": True,
            "error": None,
            "result": {
                "accessed": bool(secret.last_access),
                "provisioning_uri": secret.provisioning_uri,
                "secret": secret.secret,
            },
        }
    )


if plugin_loaded("admin_panel"):
    from ckanext.ap_main.utils import ap_before_request
    from ckanext.ap_main.views.generics import ApConfigurationPageView

    auth_admin = Blueprint("auth_admin", __name__)
    auth_admin.before_request(ap_before_request)

    auth_admin.add_url_rule(
        "/admin-panel/auth/config",
        view_func=ApConfigurationPageView.as_view(
            "config",
            "ckanext_auth_config",
            page_title=tk._("Auth config"),
        ),
    )


auth.add_url_rule(
    "/configure_2fa/<user_id>", view_func=Configure2FA.as_view("configure_2fa")
)


def get_blueprints():
    return [auth]
