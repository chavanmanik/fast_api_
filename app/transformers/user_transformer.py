from app.models import User

def transform_user(user: User):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }

def transform_users(users: list[User]):
    return [transform_user(u) for u in users]
