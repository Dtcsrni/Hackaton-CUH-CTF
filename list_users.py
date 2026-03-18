import json
import os
import sys

# Ensure we are in the right place
sys.path.append('/opt/CTFd')

from CTFd import create_app
from CTFd.models import db, Users

def list_all_users():
    app = create_app()
    with app.app_context():
        users = Users.query.all()
        user_list = [{"id": u.id, "name": u.name, "type": u.type} for u in users]
        return user_list

if __name__ == "__main__":
    try:
        users = list_all_users()
        print(json.dumps(users, indent=4))
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
