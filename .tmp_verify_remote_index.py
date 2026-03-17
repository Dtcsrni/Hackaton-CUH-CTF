from CTFd import create_app
from CTFd.models import Pages, Configs
app = create_app()
with app.app_context():
    page = Pages.query.filter_by(route='index').first()
    p = page.content or ''
    print('db_old_beige', 'color: #d2b889' in p)
    print('db_new_blue', 'color: #d7e4ef' in p)
    print('db_old_brown', 'rgba(67, 53, 45' in p)
    print('db_new_grid', 'grid-template-columns: minmax(0, 1.28fr) minmax(300px, 0.72fr);' in p)
    header = Configs.query.filter_by(key='theme_header').first()
    h = header.value or ''
    print('header_old_beige', 'color: #d2b889' in h)
    print('header_old_brown', 'rgba(67, 53, 45' in h)
