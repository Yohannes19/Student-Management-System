from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template,request,flash,redirect,url_for,abort
#from flask_migrate import Migrate

app= Flask(__name__)


      
database_link='postgresql://postgres:Meron@localhost:5432/datamodel'
app.config['SQLALCHEMY_DATABASE_URI']=database_link
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "super secret key"



db=SQLAlchemy(app)

#db.init_app(app)
#migrate = Migrate(app, db)

class students(db.Model):
    __tablename__ = 'students'
    id = db.Column('student_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))  
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))
    
def __init__(self, name, city, addr,pin):
   self.name = name
   self.city = city
   self.addr = addr
   self.pin = pin
   

  
   
@app.route('/')
def show_all():
   return render_template('show_all.html', students = students.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new_student():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['city'] or not request.form['addr']:
         flash('Please enter all the fields', 'error')
      else:
         student = students(name=request.form['name'], city=request.form['city'],
            addr=request.form['addr'],pin= request.form['pin'])
         
         db.session.add(student)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')

@app.route('/delete/<int:id>', methods = ["POST"])
def deletestud(id):
      student=students.query.get(id)
      if  student is None:
         abort(404)
      else:
         db.session.delete(student)
         db.session.commit()
         flash('Record was successfully deleted')
         return redirect(url_for('show_all'))   
   # return render_template('show_all.html')
   
@app.route('/update/<int:id>')
def updateRoute(id):
    if not id or id != 0:
        student = students.query.get(id)
        if student:
            return render_template('update.html', student=student)
   
   
@app.route('/update/<int:id>', methods = ["POST"])
def update_stu(id):
   if not id  or id!=0:
      student =students.query.get(id)
      if student:
         form=request.form
         name=form.get('name')
         city=form.get('city')
         addr=form.get('addr') 
         pin=form.get('pin')
         
         student.name=name
         student.city=city
         student.addr=addr
         student.pin=pin
         
         db.session.commit()
         flash('Data updates successfully')
         return redirect(url_for('show_all'))
   return "maybe err"


if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
   
   
   