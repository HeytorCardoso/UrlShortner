from flask import Flask, render_template, request, redirect, url_for
from database import db
from models import longUrl
import os
from dotenv import load_dotenv
from hashids import Hashids
from sqlalchemy import desc
import hashlib
import psycopg2

load_dotenv()

db_url = os.getenv("DATABASE_URL")

hashids_key = os.getenv("HASHIDS_KEY")
hashids = Hashids(salt=hashids_key, alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db.init_app(app)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        long_Url = request.form.get("urlForm", "").strip()

        if not long_Url:
            return redirect(url_for("home"))

        exists_url = longUrl.query.filter_by(long_url=long_Url).first()

        if exists_url:
            short_Url = exists_url.short_url
        else:
            try:
                data_url = longUrl(long_url=long_Url, short_url=None)
                db.session.add(data_url)
                db.session.flush()

                short_Url = hashids.encode(((data_url.id)+12000))
                data_url.short_url = short_Url
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Erro crítico: {e}")
                return "Erro ao processar sua requisição", 500

        return redirect(url_for('response', short_url=short_Url))
    return render_template("index.html")
    
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
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port)