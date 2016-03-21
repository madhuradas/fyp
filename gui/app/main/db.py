from flask.ext.sqlalchemy import SQLAlchemy

class Category(db.Model):
	__tablename__ = 'category'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text)