import json
import logging
from typing import Any, Dict

try:
    import jwt
except ImportError:
    raise ImportError(
        "PyJWT is required for the JWT plugin. Install with 'pip install pyjwt'."
    )

from auth_proxy.auth_plugins.base import AuthPlugin

logger = logging.getLogger(__name__)


class JWTAuthPlugin(AuthPlugin):
    """JWT authentication plugin for auth-proxy.

    Validates JWT tokens from the Authorization header and extracts user information.

    Configuration options:
        secret (str): Secret key for validating token signatures
        algorithm (str, optional): JWT algorithm to use. Default: "HS256"
        audience (str, optional): Expected audience claim
        issuer (str, optional): Expected issuer claim
        require_exp (bool, optional): Whether to require expiration time. Default: True
        leeway (int, optional): Leeway in seconds for expiration time. Default: 0
        header_prefix (str, optional): Authorization header prefix. Default: "Bearer"
        user_claim (str, optional): Claim to use for user identity. Default: "sub"
        role_claim (str, optional): Claim to use for role information. Default: "role"
        forward_claims (list, optional): Additional claims to forward as headers
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.secret = config.get("secret")
        if not self.secret:
            raise ValueError("JWT plugin requires a 'secret' parameter")

        self.algorithm = config.get("algorithm", "HS256")
        self.audience = config.get("audience")
        self.issuer = config.get("issuer")
        self.require_exp = config.get("require_exp", True)
        self.leeway = config.get("leeway", 0)
        self.header_prefix = config.get("header_prefix", "Bearer")
        self.user_claim = config.get("user_claim", "sub")
        self.role_claim = config.get("role_claim", "role")
        self.forward_claims = config.get("forward_claims", [])

    def authenticate(self, request_headers: Dict[str, str], path: str) -> bool:
        """Authenticate using JWT token from Authorization header.

        Args:
            request_headers: Headers from the incoming request
            path: The request path

        Returns:
            bool: True if authentication succeeds, False otherwise
        """
        auth_header = request_headers.get("Authorization", "")
        if not auth_header.startswith(f"{self.header_prefix} "):
            logger.debug(f"No {self.header_prefix} auth header found")
            return False

        token = auth_header.split(" ", 1)[1]

        try:
            options = {
                "verify_signature": True,
                "verify_exp": self.require_exp,
                "verify_aud": self.audience is not None,
                "verify_iss": self.issuer is not None,
            }

            # Store the decoded token for later use in get_auth_headers
            self._decoded_token = jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
                audience=self.audience,
                issuer=self.issuer,
                options=options,
                leeway=self.leeway,
            )

            logger.debug(f"JWT token validated successfully")
            return True

        except jwt.ExpiredSignatureError:
            logger.debug("JWT token has expired")
            return False
        except jwt.InvalidAudienceError:
            logger.debug("JWT token has invalid audience")
            return False
        except jwt.InvalidIssuerError:
            logger.debug("JWT token has invalid issuer")
            return False
        except jwt.InvalidTokenError as e:
            logger.debug(f"Invalid JWT token: {e}")
            return False
        except Exception as e:
            logger.debug(f"JWT validation error: {e}")
            return False

    def get_auth_headers(
        self, request_headers: Dict[str, str], path: str
    ) -> Dict[str, str]:
        """Add user and role information as headers after successful authentication.

        Args:
            request_headers: Headers from the incoming request
            path: The request path

        Returns:
            Dict[str, str]: Headers to add to the proxied request
        """
        if not hasattr(self, "_decoded_token"):
            return {}

        headers = {}

        # Add username from the configured claim
        if self.user_claim in self._decoded_token:
            headers["X-Auth-User"] = str(self._decoded_token[self.user_claim])

        # Add role information if available
        if self.role_claim in self._decoded_token:
            role = self._decoded_token[self.role_claim]
            if isinstance(role, list):
                headers["X-Auth-Role"] = ",".join(str(r) for r in role)
            else:
                headers["X-Auth-Role"] = str(role)

        # Forward any additional configured claims
        for claim in self.forward_claims:
            if claim in self._decoded_token:
                value = self._decoded_token[claim]
                if isinstance(value, (dict, list)):
                    # Convert complex objects to string
                    headers[f"X-Auth-Claim-{claim}"] = json.dumps(value)
                else:
                    headers[f"X-Auth-Claim-{claim}"] = str(value)

        return headers
