import hashlib
import datetime
from core.database import get_connection

class AuthService:

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def signup(self, name, email, password):
        conn = get_connection()
        cur = conn.cursor()

        hashed = self.hash_password(password)

        try:
            cur.execute(
                "INSERT INTO users (name, email, password, created_at) VALUES (?, ?, ?, ?)",
                (name, email, hashed, datetime.datetime.now().isoformat())
            )
            conn.commit()
            return True, "Signup successful!"
        except Exception as e:
            return False, f"Signup failed: {e}"
        finally:
            conn.close()

    def login(self, email, password):
        conn = get_connection()
        cur = conn.cursor()

        hashed = self.hash_password(password)

        cur.execute("SELECT id, name FROM users WHERE email=? AND password=?", (email, hashed))
        row = cur.fetchone()

        conn.close()

        if row:
            return True, {"user_id": row[0], "name": row[1]}
        else:
            return False, "Invalid email or password"
