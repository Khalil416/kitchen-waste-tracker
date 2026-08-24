import sqlite3

from fastapi import APIRouter

from backend.common.security import verify_password
from backend.db import REG_DB, connect, log
from backend.schemas.core import LoginRequest

router = APIRouter(tags=["auth"])


@router.post("/auth/login")
def auth_login(data: LoginRequest):
    log("POST /auth/login", {"username": data.username})
    try:
        conn = connect(REG_DB)
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username, role, is_active, password FROM users WHERE (username = ? OR email = ?)",
            (data.username, data.username),
        )
        row = cur.fetchone()
        conn.close()

        if not row or not verify_password(data.password, row[4]):
            return {"error": "Invalid credentials"}
        if row[3] in (0, "0"):
            return {"error": "Your account has been deactivated. Please contact your manager."}

        return {
            "success": True,
            "user_id": row[0],
            "username": row[1],
            "role": row[2],
            "is_active": bool(row[3]),
        }
    except sqlite3.Error as exc:
        return {"error": f"Login failed: {str(exc)}"}
