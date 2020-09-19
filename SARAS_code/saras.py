from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #connecting to the DB
db = SQLAlchemy(app)

class test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200),nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime,default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

##db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index', methods=['POST','GET'])

def index():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['age'] or not request.form['adr']:
            flash('Please enter all the fields', 'error')
        else:
            task_name = request.form['name']
            task_age = request.form['age']
            task_adr = request.form['adr']
            new_task  = test(name=task_name,age=task_age,address=task_adr)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/index")
        except:
            return 'There is an issue in adding the patient. Contact tech Support'
    else:
        tasks = test.query.order_by(test.date).all()
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_delete = test.query.get_or_404(id)

    try:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect('/index')
    except:
        return "Unable to delete"

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task= test.query.get_or_404(id)
    if request.method == 'POST':
        if not request.form['name'] or not request.form['age'] or not request.form['adr']:
            flash('Please enter all the fields', 'error')
        else:
            task.name = request.form['name']
            task.age = request.form['age']
            task.adr = request.form['adr']
            try:
                db.session.commit()
                return redirect('/index')
            except:
                return "Issue in Updating Task"
    else:
        return render_template('update.html',task=task)

if __name__ == "__main__":
    app.run(debug=True)