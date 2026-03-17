from CTFd import create_app
from CTFd.models import Challenges, ChallengeFiles, Pages
app=create_app()
with app.app_context():
    for name in ['Acceso por defecto','Formulario de acceso']:
        c=Challenges.query.filter_by(name=name).first()
        print(name, '=>', c.id if c else None, c.category if c else None, c.value if c else None)
        if c:
            files=ChallengeFiles.query.filter_by(challenge_id=c.id).all()
            print('files', [f.location for f in files])
    p=Pages.query.filter_by(route='bruteforce-lab').first()
    print('page', p.route if p else None, p.title if p else None, p.hidden if p else None)
