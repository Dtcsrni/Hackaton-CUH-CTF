
from CTFd import create_app
from CTFd.models import Challenges, Flags
app = create_app()
with app.app_context():
    rows = Challenges.query.order_by(Challenges.id.asc()).all()
    lengths = [(c.name, len((c.description or '').strip())) for c in rows]
    missing_flags = [c.name for c in rows if Flags.query.filter_by(challenge_id=c.id).count() == 0]
    print('challenge_count', len(rows))
    print('min_length', min(lengths, key=lambda x: x[1]))
    print('max_length', max(lengths, key=lambda x: x[1]))
    print('under_220', sum(1 for _, n in lengths if n < 220))
    print('missing_flags', missing_flags)
    for name, size in lengths[:10]:
        print('LEN', size, name)
    print('---SAMPLES---')
    for target in ['Calentamiento - Bienvenida', 'Puertas abiertas', 'Consulta concatenada', 'JWT sin audiencia', 'Perfil disperso', 'RSA sin OAEP']:
        c = Challenges.query.filter_by(name=target).first()
        snippet = (c.description or '').replace('\n', ' ')[:220]
        print(target + ' => ' + snippet)
