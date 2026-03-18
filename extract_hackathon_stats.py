import json
import os
import sys
from collections import defaultdict
from datetime import datetime

# Ensure we are in the right place
sys.path.append('/opt/CTFd')

from CTFd import create_app
from CTFd.models import db, Users, Challenges, Solves, Submissions

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
        participant_names = {u.id: u.name for u in Users.query.filter(Users.id.in_(participant_ids)).all()}

        # Basic Stats
        total_users = len(participant_ids)
        total_solves = Solves.query.filter(Solves.user_id.in_(participant_ids)).count()
        total_submissions = Submissions.query.filter(Submissions.user_id.in_(participant_ids)).count()
        
        # Curious Stats: Hourly Activity
        hourly_activity = defaultdict(int)
        all_subs = Submissions.query.filter(Submissions.user_id.in_(participant_ids)).all()
        for sub in all_subs:
            hour = sub.date.hour
            hourly_activity[hour] += 1
        
        # Curious Stats: Most persistent (most fails on a single challenge)
        fails_per_user_challenge = defaultdict(int)
        for sub in all_subs:
            if sub.type == 'incorrect':
                fails_per_user_challenge[(sub.user_id, sub.challenge_id)] += 1
        
        most_persistent = []
        for (uid, cid), count in fails_per_user_challenge.items():
            if count >= 3:
                user_name = participant_names.get(uid)
                challenge = Challenges.query.get(cid)
                if user_name and challenge:
                    most_persistent.append({
                        "user": user_name,
                        "challenge": challenge.name,
                        "fails": count
                    })
        most_persistent = sorted(most_persistent, key=lambda x: x['fails'], reverse=True)[:5]

        # Curious Stats: Most frustrating challenge (total fails)
        frustrating_challenges = defaultdict(int)
        for sub in all_subs:
            if sub.type == 'incorrect':
                frustrating_challenges[sub.challenge_id] += 1
        
        challenge_fails = []
        for cid, count in frustrating_challenges.items():
            challenge = Challenges.query.get(cid)
            if challenge:
                challenge_fails.append({
                    "name": challenge.name,
                    "fails": count
                })
        challenge_fails = sorted(challenge_fails, key=lambda x: x['fails'], reverse=True)[:5]

        # Curious Stats: Category Diversity
        user_categories = defaultdict(set)
        for sub in all_subs:
            if sub.type == 'correct':
                challenge = Challenges.query.get(sub.challenge_id)
                if challenge:
                    user_categories[sub.user_id].add(challenge.category)
        
        diversity = []
        for uid, cats in user_categories.items():
            user_name = participant_names.get(uid)
            if user_name:
                diversity.append({
                    "name": user_name,
                    "count": len(cats)
                })
        diversity = sorted(diversity, key=lambda x: x['count'], reverse=True)

        # First Bloods
        first_bloods = []
        blood_hunters = defaultdict(int)
        for c in Challenges.query.all():
            first_solve = Solves.query.filter_by(challenge_id=c.id).filter(Solves.user_id.in_(participant_ids)).order_by(Solves.date.asc()).first()
            if first_solve:
                u_name = participant_names.get(first_solve.user_id)
                if u_name:
                    blood_hunters[u_name] += 1
        
        top_blood_hunters = sorted([{"name": u, "count": c} for u, c in blood_hunters.items()], key=lambda x: x['count'], reverse=True)[:5]

        return {
            "general": {
                "total_users": total_users,
                "total_solves": total_solves,
                "total_submissions": total_submissions
            },
            "curious": {
                "hourly_activity": dict(hourly_activity),
                "most_persistent": most_persistent,
                "frustrating_challenges": challenge_fails,
                "category_diversity": diversity,
                "top_blood_hunters": top_blood_hunters
            }
        }

if __name__ == "__main__":
    try:
        stats = extract_stats()
        print(json.dumps(stats, indent=4))
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
