"""Run entry point."""

from app import create_app
from app.extensions import db
from app.models import Claim, Notification, Policy, User


app = create_app()

with app.app_context():
    db.create_all()


@app.shell_context_processor
def shell_context():
    return {"db": db, "User": User, "Policy": Policy, "Claim": Claim, "Notification": Notification}


if __name__ == "__main__":
    app.run()
