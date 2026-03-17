from CTFd import create_app
from CTFd.models import Challenges, Flags, Hints, ChallengeFiles
app=create_app()
crypto = {"XOR de respaldo","Firma reciclada","RSA sin OAEP","Derivación lenta","Bloques repetidos"}
with app.app_context():
    rows=[]
    missing=[]
    for c in Challenges.query.order_by(Challenges.id.asc()).all():
        flag_count=Flags.query.filter_by(challenge_id=c.id).count()
        if flag_count == 0:
            missing.append(c.name)
        if c.name in crypto:
            rows.append((c.name,c.category,c.value,flag_count,Hints.query.filter_by(challenge_id=c.id).count(),ChallengeFiles.query.filter_by(challenge_id=c.id).count()))
    print('missing_flags', missing)
    print('crypto_rows', rows)
