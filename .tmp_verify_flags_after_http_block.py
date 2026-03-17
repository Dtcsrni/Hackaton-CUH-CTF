from CTFd import create_app
from CTFd.models import Challenges, Flags
app = create_app()
with app.app_context():
    missing = []
    for chal in Challenges.query.order_by(Challenges.id.asc()).all():
        if Flags.query.filter_by(challenge_id=chal.id).count() == 0:
            missing.append(chal.name)
    print('challenge_count', Challenges.query.count())
    print('missing_flags', missing)
