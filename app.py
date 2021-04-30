from flask import Flask, render_template, request, flash, redirect, url_for
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from datetime import datetime

import click


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'something_secret'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Url(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True, nullable=False)
    url = db.Column(db.String(128), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Url(('id', {self.id}), ('title', {self.title}), ('url', {self.url}), ('created_at', {self.created_at}))"
 

@app.route("/", methods=['POST', 'GET'])
def root():
    if request.method == 'POST':
        title = request.form['title']
        surl = request.form['url']
        
        alert = "danger"
        msg = None

        if not title:
            msg = "title is required!"
        elif not surl:
            msg = "url is required!"
        elif Url.query.filter_by(url=surl).first() is not None:
            msg = "url already in database!"
        else:
            url = Url()
            url.title = title
            url.url = surl
            try:
                db.session.add(url)
                db.session.commit()
                msg = "Url added successfully!"
                alert = "success"
            except Exception as err:
                db.session.rollback()
                msg = f"database Error: {err}"

        flash(msg, alert)
        return redirect(url_for('root'))
    
    urls = Url.query.all()
    return render_template('index.html', urls=urls)


@app.route('/delete/<url_id>')
def delete(url_id):
    msg = None
    alert = 'danger'
    Url.query.filter_by(id=url_id).delete()
    try:
        db.session.commit()
        msg = "Url deleted successfully!"
        alert = "success"
    except Exception as err:
        db.session.rollback()
        msg = f"database Error: {err}"
    flash(msg, alert)
    return redirect(url_for('root'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
