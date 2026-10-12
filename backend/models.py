import uuid
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from sqlalchemy import event
from sqlalchemy.engine import Engine


db = SQLAlchemy()

## SQLite turns foreign keys off for every new connection; I've to switch them on each time.
@event.listens_for(Engine, "connect")
def set_sqlite_pragma (dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False, default=lambda: uuid.uuid4().hex)
    active = db.Column(db.Boolean, nullable = False, default = True)
    f_name = db.Column(db.String, nullable = False)
    l_name = db.Column(db.String, nullable = False)
    phone = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable = False, default = lambda: datetime.now(timezone.utc))

    roles = db.relationship('Role', secondary = 'roles_users', backref = 'users')

class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique = True, nullable = False)

# A junction table.
role_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), nullable=False)
)