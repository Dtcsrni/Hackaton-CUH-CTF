import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta

# Ensure we are in the right place
sys.path.append('/opt/CTFd')

from CTFd import create_app
from CTFd.models import db, Users, Challenges, Solves, Submissions

def extract_advanced_stats():
    app = create_app()
    with app.app_context():
        # Participant filter
        participant_ids_query = db.session.query(Users.id).filter(
            Users.type == "user",
            Users.banned == False,
            Users.hidden == False,
            db.func.lower(Users.name).notin_(['erick vega', 'erick renato'])
        )
        participant_ids = [uid[0] for uid in participant_ids_query.all()]
        participant_names = {u.id: u.name for u in Users.query.filter(Users.id.in_(participant_ids)).all()}

        # 1. Solving Streaks (Max solves in 60 mins)
        streaks = {}
        for uid in participant_ids:
            u_solves = Solves.query.filter_by(user_id=uid).order_by(Solves.date.asc()).all()
            max_streak = 0
            for i, s1 in enumerate(u_solves):
                current_streak = 1
                for s2 in u_solves[i+1:]:
                    if (s2.date - s1.date).total_seconds() <= 3600:
                        current_streak += 1
                    else:
                        break
                max_streak = max(max_streak, current_streak)
            streaks[participant_names[uid]] = max_streak

        # 2. Category Dominance
        cat_dominance = {}
        categories = db.session.query(Challenges.category).distinct().all()
        for (cat,) in categories:
            results = db.session.query(Users.name, db.func.count(Solves.id)).join(Solves, Solves.user_id == Users.id).join(Challenges, Challenges.id == Solves.challenge_id).filter(Challenges.category == cat, Users.id.in_(participant_ids)).group_by(Users.id).order_by(db.func.count(Solves.id).desc()).first()
            if results:
                cat_dominance[cat] = {"user": results[0], "solves": results[1]}

        # 3. Abandoned Challenges (> 5 fails, 0 solves)
        abandoned = []
        for c in Challenges.query.all():
            solves = Solves.query.filter_by(challenge_id=c.id).filter(Solves.user_id.in_(participant_ids)).count()
            fails = Submissions.query.filter_by(challenge_id=c.id, type='incorrect').filter(Submissions.user_id.in_(participant_ids)).count()
            if solves == 0 and fails > 3: # Lower threshold to 3 to see more
                abandoned.append({"name": c.name, "fails": fails})
        
        # 4. Response Speed (Avg time from 1st sub to solve)
        speeds = {}
        for uid in participant_ids:
            u_solves = Solves.query.filter_by(user_id=uid).all()
            total_time = 0
            count = 0
            for s in u_solves:
                first_sub = Submissions.query.filter_by(user_id=uid, challenge_id=s.challenge_id).order_by(Submissions.date.asc()).first()
                if first_sub:
                    diff = (s.date - first_sub.date).total_seconds()
                    total_time += diff
                    count += 1
            if count > 0:
                speeds[participant_names[uid]] = total_time / count # in seconds

        return {
            "streaks": streaks,
            "category_dominance": cat_dominance,
            "abandoned_challenges": abandoned,
            "solving_speeds": speeds
        }

if __name__ == "__main__":
    try:
        stats = extract_advanced_stats()
        with open('/tmp/advanced_results.json', 'w') as f:
            json.dump(stats, f, indent=4)
        print("SUCCESS")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
