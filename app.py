from flask import Flask, render_template
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import click


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://chaduxppgekfxg:09a540543492fffd344964c98180c3aa8d8a51ccda61a54f313a3ea8b494ba1c@ec2-54-211-176-156.compute-1.amazonaws.com:5432/dbidd3mltgi075'
db = SQLAlchemy(app)


class Url(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True, nullable=False)
    url = db.Column(db.String(128), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Url(('id', {self.id}), ('title', {self.title}), ('url', {self.url}), ('created_at', {self.created_at}))"

def init_db():
    db.create_all()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables"""
    init_db()
    click.echo("Initialized the database!")


@app.route("/")
def root():
    urls = Url.query.all()
    return render_template('index.html', urls)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
