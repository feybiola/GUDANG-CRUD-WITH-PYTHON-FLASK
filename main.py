
from flask import Flask, render_template, g, session, request, redirect, flash, url_for
from connectdb import Database


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User: {self.username}>'

users = []
users.append(User(id=1, username='Feybiola', password='password'))
users.append(User(id=2, username='Kapita', password='secret'))
users.append(User(id=3, username='Feydre', password='12345'))

app = Flask(__name__)

app.secret_key = "ini rahasia"

conn=Database('postgres')


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('home'))

        return redirect(url_for('login'))

    return render_template('login.html')
        

@app.route('/home')
def home():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('home.html')


@app.route('/logout')
def logout():
   return redirect(url_for('login'))
  
@app.route('/profile')
def profile(): 
    if not g.user:
        return redirect(url_for('login'))
    return render_template('profile.html')

@app.route("/index")
def index():
    conn = Database('postgres')
    all_data = conn.select("select * from db_feybiola")
    return render_template('index.html', barang=all_data)


@app.route("/dbInsert", methods =['POST', 'GET'])
def dbInsert():
    if request.method == 'POST':
        kode = request.form['kode']
        nama = request.form['nama']
        jenis = request.form['jenis']
        stok = request.form['stok']
        
        conn.execute("INSERT INTO db_feybiola (kode, nama, jenis, stok) VALUES ({0}, '{1}', '{2}', '{3}');".format(kode, nama, jenis, stok))
        flash('Insert Data sukses')
        return redirect (url_for("index"))

@app.route("/update/<kode>", methods = ['POST', 'GET'])
def update(kode):
    all_data=conn.select("select * from db_feybiola where kode={}".format(str(kode)))
    print(all_data[0])
    return render_template('update.html', barang=all_data[0])


@app.route("/dbUpdate/<kode>", methods = ['POST', 'GET'])
def dbUpdate(kode):
    if request.method == 'POST':
        kode = request.form['kode']
        nama = request.form['nama']
        jenis = request.form['jenis']
        stok = request.form['stok']
    
        conn.execute("update db_feybiola set nama='{0}', jenis='{1}', stok='{2}' where kode='{3}';".format(nama, jenis, stok, kode))
        flash('Data Berhasil di update')
        return redirect(url_for("index"))

@app.route('/hapus')
def hapus():
    all_data = conn.select('SELECT * from db_feybiola')
    return render_template('index.html', barang=all_data)

@app.route("/delete/<kode>", methods = ['POST','GET'])
def delete(kode):
        delete="delete from db_feybiola where kode={}".format(str(kode))
        conn.execute(delete)
        flash("Data berhasil dihapus")
        return redirect(url_for('index'))




if __name__ =="__main__" :
    app.run(port=8080, debug=True)