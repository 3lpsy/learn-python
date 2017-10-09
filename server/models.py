
# we need to import SQLAlchemy here also. Not just in our app.py!
from flask_sqlalchemy import SQLAlchemy

'''
[4] Now we create the SQLAlchemy instance.
- The SQLAlchemy instance will let us do a lot of things as its an ORM.
- An ORM let's us interact with Python classes as if the Class were table and an instance were a row in that table.
- ORM classess are typically called Models (MVC!)
- ORMS act differently depending on the language and how they are written.
- For SqlAlchemy, you can manipulate Model Instances, but when you want to save/update the database, you have to use the sqlalchemy instance's (our 'db' variable) session property. It will explained later.
'''
db = SQLAlchemy()


# Define Our SQLAlchemy Models
# The determine what database tables we can interact with.
# The existence of these classes tells SQLAlchemy which database to Create
# The properties tell SQLAlchemy which fields to create and adds some sql constraints, foreign keys

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(254), unique=False)
    is_deletable = db.Column(db.Boolean(), default=True)

    @classmethod
    def by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    # magic method that is evaluated on str(user) and print(user)
    def __repr__(self):
        return '<User %r>' % self.name

    # magic method is evaluated of if user: and bool(user)
    def __bool__(self):
        return self.id and self.id > 0

# This model has a Foreign Key to the user table.
# This means we can access the relactionship via post.author
# Relationships are awesome and save a lot of time
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(254), unique=False)
    body = db.Column(db.Text(), unique=False)
    author_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    author = db.relationship('User', backref=db.backref('posts'))

    def __repr__(self):
        return '<Post %r>' % self.title

    def __bool__(self):
        return self.id and self.id > 0
