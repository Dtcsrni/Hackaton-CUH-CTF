from CTFd import create_app
from CTFd.models import Awards, Challenges, Solves
app = create_app()
with app.app_context():
    print('first_blood_awards', Awards.query.filter_by(category='Primer solve').count())
    print('challenges_with_solves', Challenges.query.join(Solves, Solves.challenge_id == Challenges.id).distinct().count())
    for award in Awards.query.filter_by(category='Primer solve').order_by(Awards.id.asc()).limit(5).all():
        print('sample', award.name, award.value)
