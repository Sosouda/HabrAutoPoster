"""
ensure_master.py

Защитный скрипт: перед стартом воркера принудительно убеждаемся,
что Redis работает в режиме master, а не read-only replica.
"""

from redis_conn import redis_conn

info = redis_conn.info("replication")

if info.get("role") != "master":
    print(f"[ensure_master] Redis был в роли '{info.get('role')}', переключаю на master")
    redis_conn.execute_command("REPLICAOF", "NO", "ONE")
else:
    print("[ensure_master] Redis уже в роли master, всё ок")
