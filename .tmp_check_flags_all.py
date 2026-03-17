from CTFd import create_app
from CTFd.models import Challenges, Flags, Hints, ChallengeFiles
from collections import Counter
app=create_app()
with app.app_context():
    missing=[]
    bad=[]
    rows=[]
    for c in Challenges.query.order_by(Challenges.id.asc()).all():
        flag_count=Flags.query.filter_by(challenge_id=c.id).count()
        hint_count=Hints.query.filter_by(challenge_id=c.id).count()
        file_count=ChallengeFiles.query.filter_by(challenge_id=c.id).count()
        rows.append((c.name, c.category, c.value, flag_count, hint_count, file_count))
        if flag_count == 0:
            missing.append(c.name)
        if c.name in {"Perfil disperso","Agenda filtrada","Foto del laboratorio","Proveedor fantasma","Huella de publicación"} and (flag_count != 1 or hint_count != 3 or file_count < 1):
            bad.append((c.name, flag_count, hint_count, file_count))
    print('challenge_count', len(rows))
    print('missing_flags', missing)
    print('osint_checks', bad)
    print('osint_rows', [r for r in rows if r[0] in {"Perfil disperso","Agenda filtrada","Foto del laboratorio","Proveedor fantasma","Huella de publicación"}])
