"""
Middleware module for TurboAPI.

This module provides middleware components for TurboAPI applications.
"""

from typing import Callable, Optional, Sequence, Dict, List, Any

from starlette.middleware import Middleware as StarletteMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware as StarletteAuthenticationMiddleware
from starlette.requests import Request
from starlette.responses import Response

from .authentication import BaseAuthentication, AuthCredentials, UnauthenticatedUser


class Middleware:
    """
    TurboAPI middleware class.
    
    This is a simple wrapper around Starlette's Middleware class to provide
    a consistent API for turboapi users.
    """
    def __new__(cls, middleware_class: type, **options):
        """Create a new middleware instance."""
        return StarletteMiddleware(middleware_class, **options)


class AuthenticationMiddleware(StarletteAuthenticationMiddleware):
    """
    Middleware for authentication.
    
    This middleware authenticates incoming requests and attaches
    authentication information to the request.
    """
    def __init__(
        self,
        app,
        backend: BaseAuthentication,
        on_error: Callable[[Request, Exception], Response] = None
    ):
        """
        Initialize the authentication middleware.
        
        Args:
            app: The ASGI application.
            backend: The authentication backend to use.
            on_error: Optional callback for handling authentication errors.
        """
        super().__init__(app, backend, on_error)


# Custom authentication middleware implementations

class JWTAuthMiddleware(AuthenticationMiddleware):
    """
    JWT Authentication middleware.
    
    This middleware authenticates incoming requests using JWT tokens
    and attaches authentication information to the request.
    """
    def __init__(
        self,
        app,
        secret_key: str,
        algorithm: str = "HS256",
        auth_header_name: str = "Authorization",
        auth_header_type: str = "Bearer",
        user_model = None,
        token_getter = None,
        on_error: Callable[[Request, Exception], Response] = None,
        excluded_paths: List[str] = None
    ):
        """
        Initialize the JWT authentication middleware.
        
        Args:
            app: The ASGI application.
            secret_key: The secret key used to sign JWT tokens.
            algorithm: The algorithm used to sign JWT tokens.
            auth_header_name: The name of the header that contains the token.
            auth_header_type: The type of the authentication header.
            user_model: The user model to use for authenticated users.
            token_getter: Optional function to extract token from request.
            on_error: Optional callback for handling authentication errors.
            excluded_paths: List of paths to exclude from authentication.
        """
        from .authentication import JWTAuthentication
        
        backend = JWTAuthentication(
            secret_key=secret_key,
            algorithm=algorithm,
            auth_header_name=auth_header_name,
            auth_header_type=auth_header_type,
            user_model=user_model,
            token_getter=token_getter
        )
        
        self.excluded_paths = excluded_paths or []
        super().__init__(app, backend, on_error)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Dispatch the request and authenticate if needed.
        
        Args:
            request: The request to authenticate.
            call_next: The next middleware or application to call.
            
        Returns:
            The response from the next middleware or application.
        """
        # Skip authentication for excluded paths
        path = request.url.path
        if any(path.startswith(excluded) for excluded in self.excluded_paths):
            return await call_next(request)
        
        return await super().dispatch(request, call_next)


class BasicAuthMiddleware(AuthenticationMiddleware):
    """
    Basic Authentication middleware.
    
    This middleware authenticates incoming requests using HTTP Basic Authentication
    and attaches authentication information to the request.
    """
    def __init__(
        self,
        app,
        credentials: Dict[str, str],
        realm: str = "TurboAPI",
        on_error: Callable[[Request, Exception], Response] = None,
        excluded_paths: List[str] = None
    ):
        """
        Initialize the Basic authentication middleware.
        
        Args:
            app: The ASGI application.
            credentials: A dictionary mapping usernames to passwords.
            realm: The authentication realm.
            on_error: Optional callback for handling authentication errors.
            excluded_paths: List of paths to exclude from authentication.
        """
        from base64 import b64decode
        
        class BasicAuthBackend(BaseAuthentication):
            async def authenticate(self, request: Request):
                auth = request.headers.get("Authorization")
                if not auth or not auth.startswith("Basic "):
                    return AuthCredentials(), UnauthenticatedUser()
                
                try:
                    # Extract and decode the basic auth credentials
                    auth_decoded = b64decode(auth[6:]).decode("latin1")
                    username, password = auth_decoded.split(":", 1)
                    
                    # Check if credentials are valid
                    if username in credentials and credentials[username] == password:
                        return AuthCredentials(["authenticated"]), username
                except Exception:
                    pass
                
                return AuthCredentials(), UnauthenticatedUser()
        
        self.excluded_paths = excluded_paths or []
        super().__init__(app, BasicAuthBackend(), on_error)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Dispatch the request and authenticate if needed.
        
        Args:
            request: The request to authenticate.
            call_next: The next middleware or application to call.
            
        Returns:
            The response from the next middleware or application.
        """
        # Skip authentication for excluded paths
        path = request.url.path
        if any(path.startswith(excluded) for excluded in self.excluded_paths):
            return await call_next(request)
        
        return await super().dispatch(request, call_next)


class TurboAPIMiddleware:
    """
    Collection of built-in middleware generators.
    
    This class provides factory methods for common middleware configurations.
    """
    
    @staticmethod
    def cors(
        allow_origins: Sequence[str] = (),
        allow_methods: Sequence[str] = ("GET",),
        allow_headers: Sequence[str] = (),
        allow_credentials: bool = False,
        allow_origin_regex: Optional[str] = None,
        expose_headers: Sequence[str] = (),
        max_age: int = 600,
    ) -> Middleware:
        """
        Create CORS middleware for cross-origin resource sharing.
        
        Args:
            allow_origins: A list of origins that should be permitted to make cross-origin requests.
            allow_methods: A list of HTTP methods that should be allowed for cross-origin requests.
            allow_headers: A list of HTTP headers that should be allowed for cross-origin requests.
            allow_credentials: Indicate that cookies should be supported for cross-origin requests.
            allow_origin_regex: A regex string to match against origins that should be permitted.
            expose_headers: Indicate which headers are available for browsers to access.
            max_age: Maximum cache time for preflight requests (in seconds).
        
        Returns:
            Middleware instance configured for CORS.
        """
        return Middleware(
            CORSMiddleware,
            allow_origins=allow_origins,
            allow_methods=allow_methods,
            allow_headers=allow_headers,
            allow_credentials=allow_credentials,
            allow_origin_regex=allow_origin_regex,
            expose_headers=expose_headers,
            max_age=max_age,
        )
    
    @staticmethod
    def trusted_host(allowed_hosts: Sequence[str], www_redirect: bool = True) -> Middleware:
        """
        Create trusted host middleware to protect against host header attacks.
        
        Args:
            allowed_hosts: A list of host/domain names that this site can serve.
            www_redirect: If True, redirects to the same URL, but with the www. prefix.
        
        Returns:
            Middleware instance configured for trusted hosts.
        """
        return Middleware(
            TrustedHostMiddleware,
            allowed_hosts=allowed_hosts,
            www_redirect=www_redirect,
        )
    
    @staticmethod
    def gzip(minimum_size: int = 500, compresslevel: int = 9) -> Middleware:
        """
        Create gzip middleware for response compression.
        
        Args:
            minimum_size: Minimum response size (in bytes) to apply compression.
            compresslevel: Compression level from 0 to 9 (higher value = more compression).
        
        Returns:
            Middleware instance configured for gzip compression.
        """
        return Middleware(
            GZipMiddleware,
            minimum_size=minimum_size,
            compresslevel=compresslevel,
        )
    
    @staticmethod
    def https_redirect() -> Middleware:
        """
        Create middleware to redirect all HTTP connections to HTTPS.
        
        Returns:
            Middleware instance configured for HTTPS redirection.
        """
        return Middleware(HTTPSRedirectMiddleware)
        
    @staticmethod
    def authentication(backend) -> Middleware:
        """
        Create authentication middleware.
        
        Args:
            backend: The authentication backend to use.
            
        Returns:
            Middleware instance configured for authentication.
        """
        return Middleware(AuthenticationMiddleware, backend=backend)
    
    @staticmethod
    def jwt_auth(
        secret_key,
        algorithm="HS256",
        excluded_paths=None,
        user_model=None
    ) -> Middleware:
        """
        Create JWT authentication middleware.
        
        Args:
            secret_key: The secret key to use for JWT token validation.
            algorithm: The algorithm to use for JWT token validation.
            excluded_paths: A list of paths to exclude from authentication.
            user_model: The user model to use for authenticated users.
            
        Returns:
            Middleware instance configured for JWT authentication.
        """
        return Middleware(
            JWTAuthMiddleware, 
            secret_key=secret_key, 
            algorithm=algorithm,
            excluded_paths=excluded_paths,
            user_model=user_model
        )
    
    @staticmethod
    def basic_auth(
        credentials,
        realm="TurboAPI",
        excluded_paths=None
    ) -> Middleware:
        """
        Create Basic authentication middleware.
        
        Args:
            credentials: A dictionary mapping usernames to passwords.
            realm: The authentication realm.
            excluded_paths: A list of paths to exclude from authentication.
            
        Returns:
            Middleware instance configured for Basic authentication.
        """
        return Middleware(
            BasicAuthMiddleware,
            credentials=credentials,
            realm=realm,
            excluded_paths=excluded_paths
        )
