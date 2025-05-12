from flask import Flask, request, render_template
import sqlite3
import hashlib

app = Flask(__name__)




def pripoj_db():
    conn = sqlite3.connect("kurzy.db")
    return conn


@app.route('/')
def index():
    
    return render_template("stranka.html")



@app.route('/kurzy')
def zobraz_kurzy():
    conn = pripoj_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Kurzy")
    kurzy = cursor.fetchall()

    conn.close()


    return render_template("kurzy.html",kurzy=kurzy)




@app.route('/treneri')
def zobraz_trenerov():
    conn = pripoj_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT T.ID_trenera, T.Meno || ' ' || T.Priezvisko as Trener, Nazov_kurzu
        FROM Treneri T LEFT JOIN Kurzy K ON T.ID_trenera = K.ID_trenera
    """)
    treneri = cursor.fetchall()

    conn.close()

    
    return render_template("treneri.html",treneri=treneri)




@app.route('/miesta')
def zobraz_miesta():
    conn = pripoj_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Nazov_miesta FROM Miesta
    """)
    miesta = cursor.fetchall()

    conn.close()

    
    return render_template("miesta.html",miesta=miesta)





@app.route('/kapacity')
def vypis_kapacity():
    conn = pripoj_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sum(Max_pocet_ucastnikov) FROM Kurzy where Nazov_kurzu LIKE 'p%'
    """)
    kapacity = cursor.fetchall()

    conn.close()

    
    return render_template("kapacity.html",kapacity=kapacity)




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



if __name__ == '__main__':
    app.run(debug=True)


