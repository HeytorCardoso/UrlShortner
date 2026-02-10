from flask import Flask, render_template, request, redirect, url_for
from database import db
from models import longUrl
import os
from dotenv import load_dotenv
from hashids import Hashids
import hashlib
import psycopg2

load_dotenv()

db_url = os.getenv("DATABASE_URL")

hashids_key = os.getenv("HASHIDS_KEY")
hashids = Hashids(salt=hashids_key, min_length=8)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
db.init_app(app)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        long_Url = request.form["urlForm"]
        exists_url = longUrl.query.filter_by(long_url=long_Url).first()

        if exists_url:
            short_Url = exists_url.short_url
        else:
            short_Url = int.from_bytes(hashlib.sha1(long_Url.encode()).digest()[:6], "big")

        data_url = longUrl(long_url=long_Url, short_url=short_Url)
        db.session.add(data_url)
        db.session.commit()

        return redirect(url_for('response', short_url = short_Url))
    
@app.route("/response/<short_url>")
def response(short_url):
    return render_template("response.html", short_url=short_url)

@app.route("/<id>")
def link(id):
    url = db.session.query(longUrl).filter_by(short_url=id).first()
    if url:
        destiny = url.long_url
        if not destiny.startswith(('http://', 'https://')):
            destiny = f'https://{destiny}'

        return redirect(destiny)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)