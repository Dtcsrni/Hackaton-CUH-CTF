from CTFd import create_app
from CTFd.models import Challenges
app=create_app()
with app.app_context():
    rows=[(c.id,c.name,c.category,c.value,(c.description or '').strip()) for c in Challenges.query.order_by(Challenges.id.asc()).all()]
    print('count', len(rows))
    for id_,name,cat,val,desc in rows:
        print(f"{id_}	{name}	{cat}	{val}	{len(desc)}")
