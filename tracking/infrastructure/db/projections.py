from sqlalchemy import text
from .db import session_scope  # usar sesión actual

DDL = """
CREATE TABLE IF NOT EXISTS conversion_daily_status (
    day date NOT NULL,
    status varchar(16) NOT NULL,
    count bigint NOT NULL,
    PRIMARY KEY(day, status)
);
"""
UPSERT = """
INSERT INTO conversion_daily_status(day, status, count)
VALUES (CURRENT_DATE, :status, 1)
ON CONFLICT (day, status) DO UPDATE SET count = conversion_daily_status.count + 1;
"""

def ensure_projection():
    with session_scope() as s:
        s.execute(text(DDL))

def increment_status(status: str = "ok"):
    with session_scope() as s:
        s.execute(text(UPSERT), {"status": status})

def get_daily_stats():
    SQL = "SELECT day, status, count FROM conversion_daily_status ORDER BY day DESC, status"
    with session_scope() as s:
        rows = s.execute(text(SQL)).all()
        return [{"day": r[0].isoformat(), "status": r[1], "count": int(r[2])} for r in rows]
