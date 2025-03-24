import jwt
import os
from datetime import datetime, timedelta, timezone

# Load secret key from environment (or set a default for local dev)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret_key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", 60))  # Default 60 mins


def generate_jwt(user_id: str, role: str = "user", expires_in: int = JWT_EXPIRATION_MINUTES):
    """
    Generates a JWT for a given user.

    :param user_id: The user identifier (e.g., UUID or email)
    :param role: User role (default: "user")
    :param expires_in: Expiration time in minutes
    :return: Encoded JWT token
    """
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=expires_in)

    payload = {
        "sub": user_id,  # Subject (User ID)
        "role": role,  # User Role
        "exp": expiration_time.timestamp()  # Expiration time
    }

    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

#
# # Example Usage:
# if __name__ == "__main__":
#     test_token = generate_jwt(user_id="12345", role="admin")
#     print(f"Generated JWT: {test_token}")
