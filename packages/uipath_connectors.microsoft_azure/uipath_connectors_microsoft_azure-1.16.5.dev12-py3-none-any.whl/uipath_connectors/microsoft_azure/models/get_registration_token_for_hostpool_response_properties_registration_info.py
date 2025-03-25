from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

import datetime


class GetRegistrationTokenForHostpoolResponsePropertiesRegistrationInfo(BaseModel):
    """
    Attributes:
        expiration_time (Optional[datetime.datetime]): The date and time when the registration token will expire.
                Example: 2024-11-26T10:43:21.671Z.
        registration_token_operation (Optional[str]): The operation performed on the registration token. Example:
                Update.
        reset_token (Optional[bool]): Token used to reset the registration information for the hostpool.
        token (Optional[str]): The token used for registering the hostpool. Example: eyJhbGciOiJSUzI1NiIsImtpZCI6IjM2QzA
                wMUIwQTgxRDk5NTI5RERDODBFMzNFMDM3N0VCRkVDOTFERjAiLCJ0eXAiOiJKV1QifQ.eyJSZWdpc3RyYXRpb25JZCI6ImY1MjMzMTM4LTA2ODIt
                NDExZS1hODAwLWJhM2JhNDMzNzhlNCIsIkJyb2tlclVyaSI6Imh0dHBzOi8vcmRicm9rZXItZy1ldS1yMC53dmQubWljcm9zb2Z0LmNvbS8iLCJE
                aWFnbm9zdGljc1VyaSI6Imh0dHBzOi8vcmRkaWFnbm9zdGljcy1nLWV1LXIwLnd2ZC5taWNyb3NvZnQuY29tLyIsIkVuZHBvaW50UG9vbElkIjoi
                NzMwYWUxYjMtMzMxYy00YWU5LWE4ODMtOWU5YTAzN2UwOTI5IiwiR2xvYmFsQnJva2VyVXJpIjoiaHR0cHM6Ly9yZGJyb2tlci53dmQubWljcm9z
                b2Z0LmNvbS8iLCJHZW9ncmFwaHkiOiJFVSIsIkdsb2JhbEJyb2tlclJlc291cmNlSWRVcmkiOiJodHRwczovLzczMGFlMWIzLTMzMWMtNGFlOS1h
                ODgzLTllOWEwMzdlMDkyOS5yZGJyb2tlci53dmQubWljcm9zb2Z0LmNvbS8iLCJCcm9rZXJSZXNvdXJjZUlkVXJpIjoiaHR0cHM6Ly83MzBhZTFi
                My0zMzFjLTRhZTktYTg4My05ZTlhMDM3ZTA5MjkucmRicm9rZXItZy1ldS1yMC53dmQubWljcm9zb2Z0LmNvbS8iLCJEaWFnbm9zdGljc1Jlc291
                cmNlSWRVcmkiOiJodHRwczovLzczMGFlMWIzLTMzMWMtNGFlOS1hODgzLTllOWEwMzdlMDkyOS5yZGRpYWdub3N0aWNzLWctZXUtcjAud3ZkLm1p
                Y3Jvc29mdC5jb20vIiwiQUFEVGVuYW50SWQiOiJmNDMzNWY2YS0yNzBmLTQ1YTYtYTg4MS1hNDc2ZjVkNzM0MGYiLCJuYmYiOjE3MzI1MzE0MDIs
                ImV4cCI6MTczMjYxNzgwMSwiaXNzIjoiUkRJbmZyYVRva2VuTWFuYWdlciIsImF1ZCI6IlJEbWkifQ.Xn3fJ4P4piuXhzjNnSJhRkEObxoAeNU5H
                23mLC2AijxYhvGXpXuyp_ZNbNLeQkwQgySOiwF369vzUCMWTJdlKqbLHW1-sW2mgAWXQhIgC3B8GY1BZ_ngFXqeaolSNvf_L477-
                71UAzbP6VpF4ao_N_EU0OIxsC-6Oc8sK1iGHNJNu7cLeBpKY4SDWdb6YKQH3qe564hglA7zy5c1X9sH17V6joI8q0M59Su9n8_pT_JV-
                ZHQ6y1EFaplV0vPvdPrfvD6Pzck0oniIHw-LMG2P_K_6O0Kste4_-8d9GREf5e0CI90yJR2DNr6P7NeT8tFSM8sFXxoa2rtyZp_CfjRlg.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    expiration_time: Optional[datetime.datetime] = Field(
        alias="expirationTime", default=None
    )
    registration_token_operation: Optional[str] = Field(
        alias="registrationTokenOperation", default=None
    )
    reset_token: Optional[bool] = Field(alias="resetToken", default=None)
    token: Optional[str] = Field(alias="token", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetRegistrationTokenForHostpoolResponsePropertiesRegistrationInfo"],
        src_dict: Dict[str, Any],
    ):
        return cls.model_validate(src_dict)

    @property
    def additional_keys(self) -> list[str]:
        base_fields = self.model_fields.keys()
        return [k for k in self.__dict__ if k not in base_fields]

    def __getitem__(self, key: str) -> Any:
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def __delitem__(self, key: str) -> None:
        if key in self.__dict__:
            del self.__dict__[key]
        else:
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return key in self.__dict__
