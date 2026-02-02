from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eqmfo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Przedmiot(db.Model):
    __tablename__ = 'przedmioty'
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String)
    poziom = db.Column(db.Integer)
    typ = db.Column(db.String)
    atrybut = db.Column(db.String)
    profesja = db.Column(db.String)
    jakosc = db.Column(db.String)
    sloty = db.Column(db.Integer)
    opis = db.Column(db.Text)
    # Statystyki z Twojej bazy
    obrazenia = db.Column(db.Integer, default=0)
    hp = db.Column(db.Integer, default=0)
    mp = db.Column(db.Integer, default=0)
    atak = db.Column(db.Integer, default=0)
    atak_magiczny = db.Column(db.Integer, default=0)
    obrona = db.Column(db.Integer, default=0)
    obrona_magiczna = db.Column(db.Integer, default=0)
    szczescie = db.Column(db.Integer, default=0)
    szybkosc = db.Column(db.Integer, default=0)
    celnosc = db.Column(db.Integer, default=0)
    uniki = db.Column(db.Integer, default=0)
    # Dane techniczne ikonki [cite: 29, 30]
    ikonka = db.Column(db.String)
    ikonka_rzad = db.Column(db.Integer)
    ikonka_kolumna = db.Column(db.Integer)
    ikonka_wysokosc = db.Column(db.Integer)
    ikonka_szerokosc = db.Column(db.Integer)


@app.route('/')
def index():
    query = Przedmiot.query

    num_stats = ['sloty', 'obrazenia', 'hp', 'mp', 'atak', 'atak_magiczny', 'obrona', 'obrona_magiczna',
                 'szczescie', 'szybkosc', 'celnosc', 'uniki']
    for stat in num_stats:
        if request.args.get(f"{stat}_check"):
            val = request.args.get(stat, type=int)
            query = query.filter(getattr(Przedmiot, stat) >= (val if val is not None else 1))
    if request.args.get("poziom_check"):
        od = request.args.get('poziom_od', type=int)
        do = request.args.get('poziom_do', type=int)
        query = query.filter(getattr(Przedmiot, 'poziom') >= (od if od is not None else 1)) and query.filter(getattr(Przedmiot, 'poziom') <= (do if do is not None else 1))

    nazwa = request.args.get('nazwa')
    if nazwa:
        query = query.filter(Przedmiot.nazwa.contains(nazwa))

    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page=page, per_page=20, error_out=False)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('_item_list.html', items=pagination.items, pagination=pagination)

    return render_template('index.html', items=pagination.items, pagination=pagination)


if __name__ == '__main__':
    app.run(debug=True)