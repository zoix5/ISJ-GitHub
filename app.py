from flask import Flask, request, render_template
import sqlite3
import hashlib
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, instance_relative_config=True)


db_path = os.path.join(app.instance_path, "kurzy.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}".replace("\\","/")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)




def pripoj_db():
    conn = sqlite3.connect("kurzy.db")
    return conn


@app.route('/')
def index():
    
    return render_template("stranka.html")


#---------------------------------------------SqlAlchemy model -----------------------------------------------------------

class Kurz(db.Model):
    __tablename__ = "Kurzy"
    ID_kurzu              = db.Column(db.Integer, primary_key=True)
    Nazov_kurzu           = db.Column(db.String, nullable=False)
    Typ_sportu            = db.Column(db.String)
    Max_pocet_ucastnikov  = db.Column(db.Integer)
    ID_trenera            = db.Column(db.Integer)

    def __repr__(self):
        return f"<Kurz {self.Nazov_kurzu}>"




class Trener(db.Model):
    __tablename__ = "Treneri"
    ID_trenera              = db.Column(db.Integer, primary_key=True)
    Meno                    = db.Column(db.String, nullable=False)
    Priezvisko              = db.Column(db.String)
    Specializacia           = db.Column(db.String)
    Telefon                 = db.Column(db.String)

    def __repr__(self):
        return f"<Trener {self.Meno}>"
    


class Miesto(db.Model):
    __tablename__ = "Miesta"
    ID_miesta              = db.Column(db.Integer, primary_key=True)
    Nazov_miesta           = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return f"<Miesto {self.Nazov_miesta}>"
    





#--------------------------------------------------------------------------------------------------------------------------


#---------------------------------------------- Zobraz Kurzy --------------------------------------------------------------
@app.route('/kurzy')
def zobraz_kurzy():

    '''
    conn = pripoj_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Kurzy")
    kurzy = cursor.fetchall()
    conn.close()

    '''

    kurzy = Kurz.query.all()
    return render_template("kurzy.html",kurzy=kurzy)

#-----------------------------------------------------------------------------------------------------------------------------




#---------------------------------------------- Zobraz Trenérov -------------------------------------------------------------- 

@app.route('/treneri')
def zobraz_trenerov():
    '''
    conn = pripoj_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT T.ID_trenera, T.Meno || ' ' || T.Priezvisko as Trener, Nazov_kurzu
        FROM Treneri T LEFT JOIN Kurzy K ON T.ID_trenera = K.ID_trenera
    """)
    treneri = cursor.fetchall()

    conn.close()
    '''


    treneri = Trener.query.all()
    return render_template("treneri.html",treneri=treneri)


#--------------------------------------------------------------------------------------------------------------------------

    
#---------------------------------------------- Zobraz Miesta --------------------------------------------------------------


@app.route('/miesta')
def zobraz_miesta():
    '''
    conn = pripoj_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Nazov_miesta FROM Miesta
    """)
    miesta = cursor.fetchall()

    conn.close()
    '''

    miesta = Miesto.query.all()
    return render_template("miesta.html",miesta=miesta)


#--------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------- Zobraz Kapacitu --------------------------------------------------------------


@app.route('/kapacity')
def vypis_kapacity():
    '''
    conn = pripoj_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sum(Max_pocet_ucastnikov) FROM Kurzy where Nazov_kurzu LIKE 'p%'
    """)
    kapacity = cursor.fetchall()

    conn.close()
    '''


    kurzy = Kurz.query.with_entities(Kurz.Nazov_kurzu, Kurz.Max_pocet_ucastnikov).filter(Kurz.Nazov_kurzu.like('P%')).all()
    return render_template("kapacity.html",kapacity=kurzy)

#--------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------- Registrácia ---------------------------------------------------------------


@app.route('/registracia', methods=['GET'])
def registracia_form():



    return render_template("registracia.html")



@app.route('/registracia', methods=['POST'])
def registracia_trenera():

    meno = request.form['meno']
    priezvisko = request.form['priezvisko']
    specializacia = request.form['specializacia']
    telc = request.form['telefon']
    heslo = request.form['heslo']
    hashed = hashlib.sha256(heslo.encode()).hexdigest()



    conn = pripoj_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Treneri (Meno, Priezvisko, Specializacia, Telefon, Heslo) VALUES (?, ?, ?, ?, ?)", 
                   (meno, priezvisko, specializacia, telc, hashed))
    conn.commit()
    conn.close()


    return render_template("asi_zbytocne1.html")


#--------------------------------------------------------------------------------------------------------------------------


#---------------------------------------------- Pridaj kurz ---------------------------------------------------------------


@app.route('/pridajkurz', methods=['GET'])
def pridaj_form():




    return render_template("pridajkurz.html")


def sifrovanie(text):
    cislo=""
    A=5
    B=8
    for X in text:
        X = X.upper()

        cislopismena = ord(X) - ord('A')

        sifrovanie = (A*cislopismena+B)%26

        pismeno = chr(sifrovanie+ ord('A'))
        cislo+=pismeno

    return cislo




@app.route('/pridajkurz', methods=['POST'])
def pridaj_kurz():


    nazov_kurzu = request.form['nazov_kurzu']
    typ_sportu = request.form['typ_sportu']
    max_pocet_ucastnikov = request.form['max_pocet_ucastnikov']
    id_trenera = request.form['id_trenera']
    sifra_nazov = sifrovanie(nazov_kurzu)
    sifra_typ = sifrovanie(typ_sportu)

    

    conn = pripoj_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Kurzy ( Nazov_kurzu, Typ_sportu, Max_pocet_ucastnikov, ID_trenera) VALUES ( ?, ?, ?, ?)", 
                   ( sifra_nazov, sifra_typ, max_pocet_ucastnikov, id_trenera))
    conn.commit()
    conn.close()


    return render_template("asi_zbytocne2.html")

#--------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)


