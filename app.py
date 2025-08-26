from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_migrate import Migrate


            #APP

app = Flask(__name__)
app.secret_key = 'NOTEDAPPSECRET'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

            #MODElS

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


            #ROUTES

@app.route('/')
def main():
    
    sort = request.args.get('sort', 'date_desc')

    if sort == '1':
        notes = Notes.query.order_by(Notes.created_at.asc()).all()
    elif sort == '2':
        notes = Notes.query.order_by(Notes.title.asc()).all()
    elif sort == '3':
        notes = Notes.query.order_by(Notes.title.desc()).all()
    elif sort == '4':
        notes = Notes.query.order_by(Notes.created_at.desc()).all()
    else:
        notes = Notes.query.order_by(Notes.created_at.desc()).all()

    return render_template('index.html', notes=notes, sort=sort)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')

        new_note = Notes(title=title, content=content)


        db.session.add(new_note)
        db.session.commit()

        flash('Note Added Successfully', 'flash')
        return redirect(url_for('main'))
    else:
        return render_template('createnote.html')


            #RUN

@app.route('/view/<int:id>', methods=['POST', 'GET'])
def view(id):
    if request.method == "GET":
        note = Notes.query.get(id)
        return render_template('view.html', note=note)
    if request.method == "POST":
        note = Notes.query.get(id)
        note.title = request.form.get('newtitle')
        note.content = request.form.get('newcontent')
        db.session.commit()
        return redirect(url_for('main'))
    
@app.route('/delete/<int:id>')
def delete(id):
    note = Notes.query.get(id)

    db.session.delete(note)
    db.session.commit()
    flash("Note Deleted Successfully", 'flash')
    return redirect(url_for('main'))

if __name__ == "__main__":
    app.run(debug=True)




