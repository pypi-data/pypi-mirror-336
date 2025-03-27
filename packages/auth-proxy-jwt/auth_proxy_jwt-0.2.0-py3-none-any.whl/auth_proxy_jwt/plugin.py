import json
import logging
from typing import Any, Dict, List, Optional, Tuple

try:
    import jwt
except ImportError:
    raise ImportError(
        "PyJWT is required for the JWT plugin. Install with 'pip install pyjwt'."
    )

from auth_proxy.auth_plugins.base import AuthPlugin, AuthResult, PluginPath

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
        jwks_uri (str, optional): URI for JWKS (JSON Web Key Set) for dynamic key retrieval
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)

        # Required config
        self.secret = config.get("secret")
        if not self.secret and not config.get("jwks_uri"):
            raise ValueError(
                "JWT plugin requires either a 'secret' or 'jwks_uri' parameter"
            )

        # Optional config with defaults
        self.algorithm = config.get("algorithm", "HS256")
        self.audience = config.get("audience")
        self.issuer = config.get("issuer")
        self.require_exp = config.get("require_exp", True)
        self.leeway = config.get("leeway", 0)
        self.header_prefix = config.get("header_prefix", "Bearer")
        self.user_claim = config.get("user_claim", "sub")
        self.role_claim = config.get("role_claim", "role")
        self.forward_claims = config.get("forward_claims", [])
        self.jwks_uri = config.get("jwks_uri")

        # JWKS client for RS256/ES256 with dynamic keys
        self.jwks_client = None
        if self.jwks_uri:
            try:
                from jwt.jwks_client import PyJWKClient

                self.jwks_client = PyJWKClient(self.jwks_uri)
                logger.info(f"Initialized JWKS client with URI: {self.jwks_uri}")
            except ImportError:
                logger.warning(
                    "PyJWKClient not available. JWT validation with JWKS will not work."
                )
                logger.warning("Install PyJWT with 'pip install pyjwt[crypto]'")

    def authenticate(self, request_headers: Dict[str, str], path: str) -> AuthResult:
        """Authenticate using JWT token from Authorization header.

        Args:
            request_headers: Headers from the incoming request
            path: The request path

        Returns:
            AuthResult: The result of the authentication attempt
        """
        auth_header = request_headers.get("Authorization", "")
        if not auth_header.startswith(f"{self.header_prefix} "):
            logger.debug(f"No {self.header_prefix} auth header found")
            return AuthResult(authenticated=False)

        token = auth_header.split(" ", 1)[1]

        try:
            options = {
                "verify_signature": True,
                "verify_exp": self.require_exp,
                "verify_aud": self.audience is not None,
                "verify_iss": self.issuer is not None,
            }

            # Determine key to use for verification
            key = self.secret
            if self.jwks_client and (
                self.algorithm.startswith("RS")
                or self.algorithm.startswith("ES")
                or self.algorithm.startswith("PS")
            ):
                try:
                    signing_key = self.jwks_client.get_signing_key_from_jwt(token)
                    key = signing_key.key
                except Exception as e:
                    logger.error(f"Error getting signing key from JWKS: {e}")
                    return AuthResult(authenticated=False)

            # Decode and validate the token
            decoded_token = jwt.decode(
                token,
                key,
                algorithms=[self.algorithm],
                audience=self.audience,
                issuer=self.issuer,
                options=options,
                leeway=self.leeway,
            )

            logger.debug(f"JWT token validated successfully")

            # Extract authentication headers
            headers = {}

            # Add username from the configured claim
            if self.user_claim in decoded_token:
                headers["X-Auth-User"] = str(decoded_token[self.user_claim])

            # Add role information if available
            if self.role_claim in decoded_token:
                role = decoded_token[self.role_claim]
                if isinstance(role, list):
                    headers["X-Auth-Role"] = ",".join(str(r) for r in role)
                else:
                    headers["X-Auth-Role"] = str(role)

            # Forward any additional configured claims
            for claim in self.forward_claims:
                if claim in decoded_token:
                    value = decoded_token[claim]
                    if isinstance(value, (dict, list)):
                        # Convert complex objects to string
                        headers[f"X-Auth-Claim-{claim}"] = json.dumps(value)
                    else:
                        headers[f"X-Auth-Claim-{claim}"] = str(value)

            return AuthResult(authenticated=True, headers=headers)

        except jwt.ExpiredSignatureError:
            logger.debug("JWT token has expired")
            return AuthResult(authenticated=False, error="Token expired")
        except jwt.InvalidAudienceError:
            logger.debug(f"JWT token has invalid audience")
            return AuthResult(authenticated=False, error="Invalid audience")
        except jwt.InvalidIssuerError:
            logger.debug(f"JWT token has invalid issuer")
            return AuthResult(authenticated=False, error="Invalid issuer")
        except jwt.InvalidTokenError as e:
            logger.debug(f"Invalid JWT token: {e}")
            return AuthResult(authenticated=False, error=f"Invalid token: {str(e)}")
        except Exception as e:
            logger.debug(f"JWT validation error: {e}")
            return AuthResult(authenticated=False, error=f"Validation error: {str(e)}")

    def get_plugin_paths(self) -> List[PluginPath]:
        """Get paths that this plugin needs to handle.

        Returns:
            List[PluginPath]: List of paths that this plugin needs to handle
        """
        # JWT plugin doesn't need any special paths
        return []

    def handle_plugin_path(
        self, path: str, request_headers: Dict[str, str], request_body: bytes
    ) -> Optional[Tuple[int, Dict[str, str], bytes]]:
        """Handle a request to a plugin-specific path.

        Args:
            path: The request path
            request_headers: Headers from the incoming request
            request_body: Body from the incoming request

        Returns:
            Optional[Tuple[int, Dict[str, str], bytes]]: If not None, a tuple of
                (status_code, response_headers, response_body)
        """
        # JWT plugin doesn't handle any special paths
        return None
