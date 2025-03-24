import jwt
import os
import grpc
from datetime import datetime, timezone
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

# Load secret key from environment (or set a default for local dev)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret_key")
JWT_ALGORITHM = "HS256"

def authenticate_request(context):
    """
    Extracts and validates a JWT token from the gRPC metadata.
    Returns the decoded user info if valid, otherwise aborts the request.
    """

    # Extract the `authorization` header from gRPC metadata
    metadata = dict(context.invocation_metadata())
    token = metadata.get("authorization")

    if not token:
        context.abort(grpc.StatusCode.UNAUTHENTICATED, "Missing Authorization Token")

    try:
        # Decode the JWT
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

        # Ensure token is not expired
        if decoded_token.get("exp") and datetime.fromtimestamp(decoded_token["exp"], timezone.utc) < datetime.now(timezone.utc):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Token has expired")

        return decoded_token  # Return user data from the token

    except ExpiredSignatureError:
        context.abort(grpc.StatusCode.UNAUTHENTICATED, "Token has expired")
    except InvalidTokenError:
        context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")

