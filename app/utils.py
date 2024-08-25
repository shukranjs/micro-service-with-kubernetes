from datetime import datetime, timedelta, timezone

from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity


def refresh_expiring_jwts(response):
    exp_timestamp = get_jwt()["exp"]
    now = datetime.now(timezone.utc)
    target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
    if target_timestamp > exp_timestamp:
        create_access_token(identity=get_jwt_identity())

    return response
