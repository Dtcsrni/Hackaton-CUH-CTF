from pathlib import Path
import json
from CTFd import create_app
from CTFd.models import Challenges, Hints, ChallengeFiles, Pages
manifest = json.loads(Path('/tmp/safe_challenges_manifest.json').read_text(encoding='utf-8'))
app = create_app()
with app.app_context():
    ok = []
    for spec in manifest['challenges']:
        chal = Challenges.query.filter_by(name=spec['name']).first()
        assert chal is not None, spec['name']
        assert chal.category == spec['category'], spec['name']
        assert chal.value == spec['value'], spec['name']
        assert Hints.query.filter_by(challenge_id=chal.id).count() == 3, spec['name']
        assert ChallengeFiles.query.filter_by(challenge_id=chal.id).count() >= 1, spec['name']
        assert Pages.query.filter_by(route=spec['page_route']).first() is not None, spec['name']
        ok.append(spec['name'])
    print('verified_count', len(ok))
    print('first_three', ok[:3])
    print('last_three', ok[-3:])
