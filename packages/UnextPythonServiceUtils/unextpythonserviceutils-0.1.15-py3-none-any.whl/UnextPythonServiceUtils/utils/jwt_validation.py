from ast import List
import json
from jwcrypto import jwk
import jwt
from typing import Dict, List, Optional

from ..utils.exceptions import JwtValidationError
from ..utils.env_initializer import EnvStore

from ..interfaces.interfaces_th import Jwk_TH


class JwtValdationUtils:

    @staticmethod
    def __load_jwks() -> List[Jwk_TH]:
        return json.loads(EnvStore().jwks_edunew)

    @classmethod
    def _get_public_key(cls, kid: str) -> Optional[str]:
        jwks = cls.__load_jwks()
        public_key = next((key for key in jwks if key["kid"] == kid), None)
        if public_key:
            return jwk.JWK(**public_key).export_to_pem().decode("utf-8")
        return None

    @classmethod
    def validate_token(
        cls,
        token: str,
        verify_exp: bool = False,
        verify_aud: bool = False,
    ) -> Dict:
        try:
            JWT_ALGORITHM = (
                "RS256" if EnvStore().auth_token_algorithm == "RS256" else "HS256"
            )
            default_options = dict()
            if not verify_exp:
                default_options.update(verify_exp=False)
            if not verify_aud:
                default_options.update(verify_aud=False)

            unverified_header = jwt.get_unverified_header(token)
            public_key = cls._get_public_key(unverified_header["kid"])

            if not public_key:
                raise ValueError("No matching public key found")

            return jwt.decode(
                token,
                public_key,
                algorithms=[JWT_ALGORITHM],
                options=default_options,
            )
        except jwt.ExpiredSignatureError:
            raise JwtValidationError("Token has expired")
        except jwt.InvalidSignatureError:
            raise JwtValidationError("Invalid token: Signature verification failed")
        except jwt.InvalidAudienceError:
            raise JwtValidationError(
                "Invalid token: Audience claim verification failed"
            )
        except jwt.InvalidIssuerError:
            raise JwtValidationError("Invalid token: Issuer claim verification failed")
        except jwt.DecodeError:
            raise JwtValidationError("Malformed token: Unable to decode")
        except jwt.PyJWTError as e:
            raise JwtValidationError(f"Invalid token: {str(e)}")
        except Exception as e:
            raise JwtValidationError("Internal server error during token validation")
