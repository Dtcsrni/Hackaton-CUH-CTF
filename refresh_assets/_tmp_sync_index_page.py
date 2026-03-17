from pathlib import Path
from CTFd import create_app
from CTFd.cache import clear_pages
from CTFd.models import Pages, db

content = Path('/tmp/index.html').read_text(encoding='utf-8')
app = create_app()
with app.app_context():
    page = Pages.query.filter_by(route='index').first()
    if page is None:
        raise SystemExit('index page not found')
    page.content = content
    page.title = 'Hackatón OSINT + CTF CUH 2026'
    page.draft = False
    page.hidden = False
    page.auth_required = False
    db.session.commit()
    clear_pages()
    print('index synced')
