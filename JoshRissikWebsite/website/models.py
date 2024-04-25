from . import db

class Admin(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    properties = db.relationship('Property', backref='admin', lazy=True)

class Property(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False, unique=False)
    bedrooms = db.Column(db.Float(), nullable=False, unique=False)
    bathrooms = db.Column(db.Float(), nullable=False, unique=False)
    description = db.Column(db.String(), nullable=True, unique=False)
    price = db.Column(db.Float(), nullable=False, unique=False)
    address = db.Column(db.String(), nullable=False, unique=False)
    url_link = db.Column(db.String(), nullable=True, unique=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    thumbnail = db.Column(db.String(), nullable=True)
    image2 = db.Column(db.String(), nullable=True)
    image3 = db.Column(db.String(), nullable=True)
