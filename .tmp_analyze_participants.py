from collections import defaultdict, Counter
from statistics import median
from CTFd import create_app
from CTFd.models import db
app = create_app()
with app.app_context():
    reason_rows = db.session.execute(db.text("SELECT reason, COUNT(*) FROM ctfcu_solve_evidence_requirements GROUP BY reason ORDER BY COUNT(*) DESC" )).fetchall()
    print('reason_counts', reason_rows)

    user_rows = db.session.execute(db.text("SELECT u.id, u.name, COUNT(*) AS rapid_count, SUM(c.value) AS rapid_points FROM ctfcu_solve_evidence_requirements r JOIN users u ON u.id=r.user_id JOIN challenges c ON c.id=r.challenge_id GROUP BY u.id, u.name ORDER BY rapid_count DESC, rapid_points DESC" )).fetchall()
    print('rapid_by_user', user_rows)

    solve_rows = db.session.execute(db.text("SELECT u.name, c.name, c.value, r.elapsed_seconds, r.reason, r.solved_at FROM ctfcu_solve_evidence_requirements r JOIN users u ON u.id=r.user_id JOIN challenges c ON c.id=r.challenge_id ORDER BY u.name, r.solved_at ASC" )).fetchall()
    per_user = defaultdict(list)
    for row in solve_rows:
        per_user[row[0]].append(row)
    burst_rows = []
    for user, rows in per_user.items():
        if len(rows) < 3:
            continue
        deltas = []
        for idx in range(1, len(rows)):
            prev = rows[idx-1][5]
            cur = rows[idx][5]
            deltas.append(int((cur - prev).total_seconds()))
        burst_rows.append((user, len(rows), median(deltas) if deltas else None, min(deltas) if deltas else None))
    burst_rows.sort(key=lambda item: (-item[1], item[2] if item[2] is not None else 10**9))
    print('burst_rows', burst_rows)

    shared_ip_rows = db.session.execute(db.text("SELECT ip, COUNT(DISTINCT user_id) AS user_count, GROUP_CONCAT(DISTINCT user_id ORDER BY user_id) AS user_ids FROM submissions WHERE ip IS NOT NULL AND ip != '' GROUP BY ip HAVING COUNT(DISTINCT user_id) > 1 ORDER BY user_count DESC, ip ASC" )).fetchall()
    print('shared_ips', shared_ip_rows[:20])

    open_gap_rows = db.session.execute(db.text("SELECT u.name, COUNT(*) FROM ctfcu_solve_evidence_requirements r JOIN users u ON u.id=r.user_id WHERE r.reason='missing-open-tracking' GROUP BY u.name ORDER BY COUNT(*) DESC" )).fetchall()
    print('missing_open_tracking', open_gap_rows)
