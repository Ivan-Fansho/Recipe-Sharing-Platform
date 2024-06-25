from .models import User
from sqlalchemy.orm import Session
from ..api.authentication.authentication_service import hash_pass


def initialize_special_accounts(db: Session):
    admin = db.query(User).filter_by(username="admin").first()
    if not admin:
        admin = User(
            username="admin",
            password=hash_pass("Admin1!!"),
            email="kis.team.telerik@gmail.com",
            is_admin=True,
            is_restricted=False,
        )
        db.add(admin)
        db.commit()