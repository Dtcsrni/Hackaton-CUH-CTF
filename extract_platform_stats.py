import json
import os
import sys
from collections import defaultdict

# Ensure we are in the right place
sys.path.append('/opt/CTFd')

from CTFd import create_app
from CTFd.models import db, Users, Challenges, Solves, Submissions, Hints, Tags, HintUnlocks, Fails, Awards, Pages

def extract_stats():
    app = create_app()
    with app.app_context():
        # Define participant filter
        participant_ids_query = db.session.query(Users.id).filter(
            Users.type == "user",
            Users.banned == False,
            Users.hidden == False,
            db.func.lower(Users.name).notin_(['erick vega', 'erick renato'])
        )
        participant_ids = [uid[0] for uid in participant_ids_query.all()]

        # Hints Usage
        total_hints_unlocked = HintUnlocks.query.filter(HintUnlocks.user_id.in_(participant_ids)).count()
        
        # Tag Distribution
        tag_dist = defaultdict(int)
        for t in Tags.query.all():
            tag_dist[t.value] += 1
        
        # Fails (incorrect submissions)
        total_fails = Fails.query.filter(Fails.user_id.in_(participant_ids)).count()
        
        # Awards given (if any)
        total_awards = Awards.query.filter(Awards.user_id.in_(participant_ids)).count()
        
        # Pages in the platform
        total_pages = Pages.query.count()

        return {
            "platform": {
                "total_hints_unlocked": total_hints_unlocked,
                "tag_distribution": dict(tag_dist),
                "total_fails": total_fails,
                "total_awards": total_awards,
                "total_pages": total_pages,
                "total_challenges": Challenges.query.count()
            }
        }

if __name__ == "__main__":
    try:
        stats = extract_stats()
        with open('/tmp/platform_results.json', 'w') as f:
            json.dump(stats, f, indent=4)
        print("SUCCESS")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
