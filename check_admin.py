import json
import os
import sys

# Ensure we are in the right place
sys.path.append('/opt/CTFd')

from CTFd import create_app
from CTFd.models import db, Users, Solves, Submissions

def check_admin_activity():
    app = create_app()
    with app.app_context():
        # Get users that are NOT type 'user'
        admins = Users.query.filter(Users.type != "user").all()
        admin_ids = [u.id for u in admins]
        
        admin_solves = Solves.query.filter(Solves.user_id.in_(admin_ids)).count()
        admin_subs = Submissions.query.filter(Submissions.user_id.in_(admin_ids)).count()
        
        return {
            "admins": [{"id": u.id, "name": u.name} for u in admins],
            "admin_solves": admin_solves,
            "admin_submissions": admin_subs
        }

if __name__ == "__main__":
    try:
        activity = check_admin_activity()
        print(json.dumps(activity, indent=4))
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
