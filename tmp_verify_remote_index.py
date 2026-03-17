from CTFd import create_app
from CTFd.models import Configs, Pages

app = create_app()

with app.app_context():
    page = Pages.query.filter_by(route="index").first()
    header = Configs.query.filter_by(key="theme_header").first()
    content = page.content or ""
    theme_header = header.value or ""
    checks = {
        "db_old_beige": "color: #d2b889" in content,
        "db_new_blue": "color: #d7e4ef" in content,
        "db_old_brown": "rgba(67, 53, 45" in content,
        "db_old_side": "rgba(222, 210, 193, 0.82)" in content,
        "db_new_side": "rgba(222, 229, 235, 0.82)" in content,
        "db_new_grid": "grid-template-columns: minmax(0, 1.28fr) minmax(300px, 0.72fr);" in content,
        "header_old_beige": "color: #d2b889" in theme_header,
        "header_old_brown": "rgba(67, 53, 45" in theme_header,
    }
    for key, value in checks.items():
        print(f"{key}={value}")

    needles = [
        "color: #d2b889",
        "rgba(222, 210, 193, 0.82)",
        "rgba(67, 53, 45",
    ]
    for cfg in Configs.query.all():
        blob = cfg.value or ""
        hits = [needle for needle in needles if needle in blob]
        if hits:
            print(f"config_hit key={cfg.key} needles={hits}")
