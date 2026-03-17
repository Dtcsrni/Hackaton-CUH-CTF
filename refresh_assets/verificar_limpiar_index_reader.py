import re
from CTFd import create_app
from CTFd.models import Configs, db


def strip_block(value: str, start: str, end: str) -> str:
    return re.sub(re.escape(start) + r".*?" + re.escape(end), "", str(value), flags=re.S).strip()


app = create_app()
with app.app_context():
    header = Configs.query.filter_by(key="theme_header").first()
    footer = Configs.query.filter_by(key="theme_footer").first()
    header.value = strip_block(header.value, "<!-- CTFCU_INDEX_READER_STYLE_START -->", "<!-- CTFCU_INDEX_READER_STYLE_END -->")
    footer.value = strip_block(footer.value, "<!-- CTFCU_INDEX_READER_SCRIPT_START -->", "<!-- CTFCU_INDEX_READER_SCRIPT_END -->")
    db.session.commit()
    print("HEADER_HAS_MARKER", "CTFCU_INDEX_READER_STYLE_START" in (header.value or ""))
    print("FOOTER_HAS_MARKER", "CTFCU_INDEX_READER_SCRIPT_START" in (footer.value or ""))
