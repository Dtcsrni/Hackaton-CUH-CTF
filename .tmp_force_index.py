from pathlib import Path
from CTFd import create_app
from CTFd.cache import clear_pages
from CTFd.models import Pages, db
app = create_app()
with app.app_context():
    page = Pages.query.filter_by(route='index').first()
    if page is None:
        raise SystemExit('index page not found')
    page.content = Path('/tmp/index_cuh_latest.html').read_text(encoding='utf-8')
    db.session.commit()
    clear_pages()
    print('index forced')
