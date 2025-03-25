"""
TurboAPI: A high-performance web framework with elegant syntax and powerful validation.

Built on Starlette and using satya for data validation.
"""

__version__ = "0.2.8"

from .applications import TurboAPI
from .routing import APIRouter
from .params import Path, Query, Header, Cookie, Body, Depends, Security
from .responses import JSONResponse, HTMLResponse, PlainTextResponse, RedirectResponse, Response
from starlette.requests import Request
# Import middleware directly from appropriate locations
from starlette.middleware.authentication import AuthenticationMiddleware
from .middleware import Middleware
# Import authentication middleware directly from our middleware module
from .authentication import (
    AuthCredentials, 
    BaseUser, 
    SimpleUser, 
    UnauthenticatedUser,
    BaseAuthentication,
    JWTAuthentication,
    OAuth2PasswordRequestForm,
    OAuth2PasswordBearer
)
# Define JWT and Basic auth middleware here
from .middleware import BasicAuthMiddleware, JWTAuthMiddleware
from .exceptions import HTTPException
from .background import BackgroundTasks

# For WebSocket support
from starlette.websockets import WebSocket
