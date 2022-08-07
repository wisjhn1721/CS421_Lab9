import os
from flask import Flask, render_template, flash
from forms import StudentGradeForm, RemoveGradeForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'securityKey'
# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grades.db'
app.config['SQLALCHEMY_TRAC_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# define our models
class Grades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    grade = db.Column(db.Float(asdecimal=True))


@app.route('/', methods=['GET', 'POST'])
def home():
    form = StudentGradeForm()
    remove_form = RemoveGradeForm()
    if form.validate_on_submit():
        student = Grades.query.filter_by(name=form.name.data).first()
        if student is None:
            midterm1 = form.midterm1.data
            midterm2 = form.midterm2.data
            final = form.final.data
            avg_grade = (midterm1 + midterm2 + 2*final) / 4
            student = Grades(name=form.name.data, grade=avg_grade)
            db.session.add(student)
            db.session.commit()
        else:
            flash('Student\'s grade was already submitted')

        name = form.name.data
        form.name.data = ''
        form.midterm1.data = ''
        form.midterm2.data = ''
        form.final.data = ''
        flash(name+"'s grade was successfully submitted")
    return render_template('home.html', form=form, remove_form=remove_form)


@app.route('/remove', methods=['POST'])
def remove():
    form = StudentGradeForm()
    remove_form = RemoveGradeForm()
    if remove_form.validate_on_submit():
        student = Grades.query.filter_by(id=remove_form.id.data).first()
        name = student.name
        print(student)
        print("Students name: ", name)
        Grades.query.filter_by(id=remove_form.id.data).delete()
        db.session.commit()

        flash(name+"'s grade was successfully removed!")
    return render_template('home.html', form=form, remove_form=remove_form)


@app.route('/allgrades')
def grades():
    students = Grades.query.all()
    form = StudentGradeForm()
    return render_template('results.html', students=students, form=form)


@app.route('/update', methods=['POST'])
def update():
    students = Grades.query.all()
    form = StudentGradeForm()
    if form.validate_on_submit():
        student = Grades.query.filter_by(name=form.name.data).first()
        midterm1 = form.midterm1.data
        midterm2 = form.midterm2.data
        final = form.final.data
        avg_grade = (midterm1 + midterm2 + 2 * final) / 4
        student.grade = avg_grade
        db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.midterm1.data = ''
        form.midterm2.data = ''
        form.final.data = ''
        flash(name+"'s grade has been updated")

    return render_template('results.html', students=students, form=form)


if __name__ == '__main__':
    app.run()


