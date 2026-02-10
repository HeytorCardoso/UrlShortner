from database import db

class longUrl (db.Model):
    __tablename__ = "list_urls"

    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(256), nullable=False, unique=True)
    short_url = db.Column(db.String(256), nullable=True, unique=True)

    def __repr__(self):
        return f"<{self.long_url}>"