from __future__ import annotations

import logging
from datetime import datetime as dt
from datetime import timezone as tz
from typing import Any, cast

import pyotp
from sqlalchemy import Column, DateTime, ForeignKey, Text
from typing_extensions import Self

import ckan.model as model
import ckan.plugins.toolkit as tk
from ckan.model.types import make_uuid

import ckanext.auth.config as auth_config
from ckanext.auth.exceptions import ReplayAttackException

log = logging.getLogger(__name__)


class UserSecret(tk.BaseModel):
    __tablename__ = "2fa_user_secret"

    id = Column(Text, primary_key=True, default=make_uuid)
    user_id = Column(ForeignKey(model.User.id, ondelete="CASCADE"), primary_key=True)
    secret = Column(Text, nullable=False)
    last_access = Column(DateTime)

    @classmethod
    def create_for_user(cls, user_name: str) -> Self:
        """Creates a new security challenge for the user

        Args:
            user_name (str | None): user name

        Raises:
            ValueError: if the user_name is not provided

        Returns:
            Self: the new security challenge
        """
        secret_value = pyotp.random_base32()
        user_secret = cls.get_for_user(user_name)

        user = (
            model.Session.query(model.User).filter(model.User.name == user_name).first()
        )

        if not user:
            raise tk.ObjectNotFound("User not found")

        if not user_secret:
            user_secret = cls(user_id=user.id, secret=secret_value)
        else:
            user_secret.secret = secret_value

        model.Session.add(user_secret)
        model.Session.commit()

        return user_secret

    @classmethod
    def get_for_user(cls, user_name: str) -> Self | None:
        """Finds a secret object using the user name
        :raises ValueError if the user_name is not provided
        """

        user = model.User.get(user_name)

        if not user:
            raise tk.ObjectNotFound("User not found")

        return (
            model.Session.query(cls)
            .join(model.User, model.User.id == cls.user_id)
            .filter(model.User.id == user.id)
            .first()
        )

    def get_code(self) -> str:
        """Get the current code for the secret"""
        return pyotp.TOTP(
            cast(str, self.secret),
            interval=auth_config.get_2fa_email_interval(),
        ).now()

    def check_code(self, code: str, verify_only=False):
        """Check the code against the secret

        Args:
            code (str): the code to check
            verify_only (bool, optional): if True, the code is not saved as a successful challenge. Defaults to False.

        Raises:
            ReplayAttackException: if the code has already been used

        Returns:
            bool: True if the code is valid, False otherwise
        """
        is_totp_enabled = auth_config.is_totp_2fa_enabled()

        if is_totp_enabled:
            totp = pyotp.TOTP(cast(str, self.secret))
            # valid_window – extends the validity to this many counter ticks
            # before and after the current one
            result = totp.verify(code, valid_window=1)
        else:
            totp = pyotp.TOTP(
                cast(str, self.secret), interval=auth_config.get_2fa_email_interval()
            )
            result = totp.verify(code)

        if result and not verify_only:
            # check for replay attack...
            if (
                is_totp_enabled
                and self.last_access
                and totp.at(cast(dt, self.last_access)) == code
            ):
                raise ReplayAttackException("The code has already been used")

            self.last_access = dt.now(tz.utc)
            model.Session.commit()
        else:
            log.debug("2FA: Failed to verify the totp code for user %s", self.user_id)

        return result

    @property
    def provisioning_uri(self):
        """Returns the uri for setting up a QR code"""
        user = (
            model.Session.query(model.User)
            .filter(model.User.id == self.user_id)
            .first()
        )

        if user is None:
            raise ValueError(
                "No user found for UserSecret instance with user_id {}".format(
                    self.user_id
                )
            )

        return pyotp.TOTP(cast(str, self.secret)).provisioning_uri(
            user.name, issuer_name=tk.config["ckan.site_url"]
        )
