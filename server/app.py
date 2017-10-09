# import core python modules, these modules/packages are installed with python
import os

# import Flask packages
from flask import Flask, make_response, render_template, request, redirect, url_for, flash, json

# import Flask Extensions
from flask_sqlalchemy import SQLAlchemy
# import sqlalchemy helper
from sqlalchemy.orm import lazyload

# import some helpers
from utils import model_to_dict
# notice how we write our imports in the order advised in main.py

''' ------------ HELPER VARIABLES -------- '''


# [0] Let's define a utility variable to get a path to the project directory (the server directory)
# Notice that we've made these variables uppercase. By convention (best practice), uppercase variables mean constants (variables that will never change). But just because it is lowercase, doesn't mean that it will change.
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(PROJECT_PATH, 'db.sqlite')

''' ------------ THE FLASK AND FLASK EXTENSION INSTANCES ----- '''
# [1] Create Our Flask Instance.
# - We've imported the Flask class from the flask module.
# - Now we need to initialize that class and create an instance
# - When initializing a class, you use the ClassName() format.
# - This will invoke the __init__(self ...) method on the class and return an instance.
# - You can pass in arguments to __init__ method (we call this a constructor sometimes)
# - Typically can be passed inline like ClassName(foo)
# - Sometimes they can be passed in as key valu pairs like ClassName(bar='baz')
# - And of course you can do both like ClassNmae(foo, bar='baz')
# - It depends on how the __init__ method is writter. you can actually do this with any method/function. But the function has to be defined in a way to allow it. There are also other things like using *args and **kwargs but I will not go into them

# We pass it the template_folder param (the folder holds our html/jinja templates)
# This way render_template knows where to look for templates
app = Flask(__name__, template_folder='templates')

# Create a Secret Key
# This allows to use flask's built in flash messages
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

'''
[2] Sqlite needs a URI. The URI for sqlite is based off path to the sqlite file.
- For mysql, it woud be something liek 'mysql://username:password@hostname:port/databasename'
- But we're using sqlite so it looks a bit different and uses the file path
'''
db_uri = 'sqlite:///{}'.format(DB_PATH)

'''
[3] The flask app has a configuaration dictionary as property.
- Class properties are similar to methods except they hold values and do not perform logic.
- A property can be anything (string, int, dict, instance of another class etc).
- There are many built in config values that will tell flask to do certain things.
- In fact, we could actually define our templates dir here as opposed to in the constructor above.
- However, Flask extensions like sqlalchemy, can also access flask configs.
- So let's set some 'SQLALCHEMY_DATABASE_URI' value on our flask instance as sqlalchemy will expect it.
'''
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

# this is configuration to remove a debug message
# dont' worry about it, and it's not necessary. It just removes an unnecessary warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db, User, Post

'''
[4] WHAT ! Why would you import something down here? Why not up top?
- Well I wanted you to read this from top to bottom. And not clutter things up but yes it should go up top but this is fine.
- First, I'll explain that this import imports two types of things from our models file.
- It imports the SqlAlchemy instance (the db variable) and our models).
- These are very import so go read the models.py file before continueing (start at [0]).
- Also note We import 'db' here then 'db' is imported in our main.py file from here.
- It's like a chained import. Pretty neat.
'''

'''
[5] We have to attach our app to our sqlalchemy instance. How else would you know about that 'SQLALCHEMY_DATABASE_URI' value that we defined on our app?
- Most flask extensions have an init_app() method. This is not the constructor of the class!
- The init_app method is just way to handle configuration and register the extension on the app.
'''
db.init_app(app)

'''
[6] Again, I imported down here for clarity. These are helper methods that flask gives to do a few things:
- request lets us access the current request (GET, POST etc). It's very important.
- make_response helps user create valid HTTP response (adds HTTP headers, cookies etc)
- render_template helps us create the html. We can pass data to it that will modify our html.
- Remember! HTML is static on the server. Our html files are actually jinja2 files that render_template converts into html.
'''
from flask import request, make_response, render_template



''' ------------ APPLICATION ROUTES -------- '''

# [7] Read Through Each Application route
# - Trigger each Application Route in the Browser
# - Print out the request data being sent


'''
Request: http://IP/
Response: A page that shows our home page.
Methods: Any Method
'''
@app.route('/')
def home_index():
    return make_response(render_template('home.html'))

'''
Request: http://IP/post
Response: A page that shows a table of all of our blog posts.
Methods: Any Method
'''
@app.route('/post')
def post_index():
    # The typical command to get all posts:
    # posts = Post.query.all()
    # however we want to load the relationship as well so we will do:
    posts = Post.query.options(lazyload('author')).all()
    # this will do a sql join so that the author will already be loaded
    # this way if we do post.author in our template, it will not need to
    # make another sql query because the author will already be on the python object.
    # If our client (browser or cli) wants json, we need to convert our list of model instances
    # to json
    if 'application/json' in request.headers.get('Accept'):
        # to jsonify a sqlalchemy model instance, we first convert it to a dict
        # model_to_dict is defined in utils.py
        # the [method(val) for val in list] format is called list comprehension
        # it's pretty cool and lets us do awesome stuff in one like
        return json.jsonify([model_to_dict(post) for post in posts])
    return make_response(render_template('post_index.html', posts=posts))


'''
Request: http://IP/post/create
Purpose: Return a page that shows the create form for a post.
Methods: GET
'''
@app.route('/post/create', methods=['GET'])
def post_create():
    # TODO: check if it wants json and return json, not HTML
    users = User.query.all()
    if 'application/json' in request.headers.get('Accept'):
        # we can't return json of an html page, that doesn't make sense
        # so lets just tell the client that wants json (CLI) that we don't
        # know how to do that.
        return make_response(json.jsonify({'message': 'Not Implemented'}), 404)
    return make_response(render_template('post_create.html', users=users))

'''
Request: http://IP/post
Purpose: Create a Post and redirect by the post_show route
Methods: POST
'''
@app.route('/post', methods=['POST'])
def post_store():
    # get the form data from the request
    # the keys are the same as the 'name'attribute on the html input element
    body = request.form.get('body')
    title = request.form.get('title')
    post = Post(body=body, title=title)
    author_id = request.form.get('author_id')
    if author_id and int(author_id) > 0:
        author = User.query.get(author_id)
        # TODO: Return 404 if it doesn't exists
        post.author = author
    else:
        author = User.by_name('anonymous')
        post.author = author

    db.session.add(post)
    db.session.commit()
    message = 'Post Created!'
    if 'application/json' in request.headers.get('Accept'):
        return make_response(json.jsonify({'message': message}), 200)
    flash(message, 'info')
    # let's redirect to the show route and view our recently updated post
    return redirect(url_for('post_show', post_id=post.id))

'''
Request: http://IP/post/%post_id%
Purpose: Return a page that shows the title and body of a single post.
Methods: GET
Params:
    - post_id: the sql id of our post we wish to view

- Notice how post_id is passed to the post_show method.
- The @app.route decorator does this for us. Neat!
'''
@app.route('/post/<int:post_id>', methods=['GET'])
def post_show(post_id):
    post = Post.query.get(post_id)
    # notice that we didn't lazy load the author like we did in index.
    if not post:
        message = "Post {} Does not Exist".format(post_id)
        # return json if it wants it
        if 'application/json' in request.headers.get('Accept'):
            return make_response(json.jsonify({'message': message}), 404)
        flash(message, 'danger')
        return redirect(url_for('post_index'))
    if 'application/json' in request.headers.get('Accept'):
        # convert post to html for CLI clients
        return make_response(json.jsonify(model_to_dict(post)), 200)
    return make_response(render_template('post_show.html', post=post))


'''
Request: http://IP/post/%post_id%/edit
Purpose: Return a page that shows the title and body of a single post.
Methods: GET
Params:
    - post_id: the sql id of our post we wish to view

- Notice how post_id is passed to the post_show method.
- The @app.route decorator does this for us. Neat!
'''
@app.route('/post/<int:post_id>/edit', methods=['GET'])
def post_edit(post_id):
    # check if post even exists
    post = Post.query.get(post_id)
    if not post:
        message = "Post {} Does not Exist".format(post_id)
        flash(message, 'danger')
        if 'application/json' in request.headers.get('Accept'):
            return make_response(json.jsonify({'message': message}), 404)
        return redirect(url_for('post_index'))
    post = Post.query.get(post_id)
    users = User.query.all()
    # notice that we didn't lazy load the author. We could and probably should.
    # TODO: check if it wants json and return json, not HTML
    if 'application/json' in request.headers.get('Accept'):
        # we can't convert html to json
        return make_response(json.jsonify({'message': 'Not Implemented'}), 404)
    return make_response(render_template('post_edit.html', post=post, users=users))


'''
Request: http://IP/post/%post_id%
Purpose: Update a Post and redirect by the post_show route
Methods: POST
Params:
    - post_id: the sql id of our post we wish to view
- Note that many apps would use a PUT or PATH method, but we can just POST as PUT and PATCH are not implemented everywhere.
'''
@app.route('/post/<int:post_id>', methods=['POST'])
def post_update(post_id):
    # check if post even exists
    post = Post.query.get(post_id)
    if not post:
        message = "Post {} Does not Exist".format(post_id)
        flash(message, 'danger')
        if 'application/json' in request.headers.get('Accept'):
            return make_response(json.jsonify({'message': message}), 404)
        return redirect(url_for('post_index'))
    # get data from request
    post.body = request.form.get('body')
    post.title = request.form.get('title')
    author_id = request.form.get('author_id')
    if author_id and int(author_id) > 0:
        author = User.query.get(author_id)
        # TODO: Return 404 if it doesn't exists
        post.author = author
    else:
        author = User.by_name('guest')
        post.author = author
    db.session.add(post)
    db.session.commit()
    message = 'Post Updated!'
    if 'application/json' in request.headers.get('Accept'):
        return make_response(json.jsonify({'message': message}), 200)
    # Many frameworks implement a form of 'flashing' where a message or text can be accessed in the next request and only the next request. Here, when the app redirects, we'll be able to access this message.
    # We'll display the message in flash_messages.html
    flash(message, 'info')
    # let's redirect to the show route and view our recently updated post

    return redirect(url_for('post_show'))

'''
Request: http://IP/post/%post_id%/destroy
Purpose: Delete a Post and redirect by the post_index route
Methods: POST
Params:
    - post_id: the sql id of our post we wish to view
- Note many apps use a DELETE HTTP method. We will just use a POST method.
- Do not use a get method for deleteing items
'''
@app.route('/post/<int:post_id>/destroy', methods=['POST'])
def post_destroy(post_id):
    # check if post even exists
    post = Post.query.get(post_id)
    if not post:
        message = "Post {} Does not Exist".format(post_id)
        flash(message, 'danger')
        if 'application/json' in request.headers.get('Accept'):
            return make_response(json.jsonify({'message': message}), 404)
        return redirect(url_for('post_index'))

    db.session.delete(post)
    db.session.commit()
    message = 'Post Deleted!'
    if 'application/json' in request.headers.get('Accept'):
        return make_response(json.jsonify({'message': message}), 200)
    # let's redirect to the show route and view our recently updated post
    flash(message, 'info')
    return redirect(url_for('post_index'))

'''
Request: http://IP/user
Response: A page that shows a table of all of our authors (users).
Methods: Any Method
'''
@app.route('/user')
def user_index():
    users = User.query.all()
    if 'application/json' in request.headers.get('Accept'):
        return json.jsonify([model_to_dict(user) for user in users])
    return make_response(render_template('user_index.html', users=users))

'''
Request: http://IP/post/%post_id%
Purpose: Return a page that shows the users details.
Methods: GET
Params:
    - user_id: the sql id of our user we wish to view
'''
@app.route('/user/<int:user_id>', methods=['GET'])
def user_show(user_id):
    user = User.query.get(user_id)
    # notice that we didn't lazy load the author like we did in index.
    if not user:
        message = "User {} Does not Exist".format(user_id)
        # return json if it wants it
        if 'application/json' in request.headers.get('Accept'):
            return make_response(json.jsonify({'message': message}), 404)
        flash(message, 'danger')
        return redirect(url_for('user_index'))
    if 'application/json' in request.headers.get('Accept'):
        # convert user to json for CLI clients
        return make_response(json.jsonify(model_to_dict(user)), 200)
    return make_response(render_template('user_show.html', user=user))


# what is we called "$ python app.py" here? What would be evaluated? We wouldn't see any output, but does that mean nothing is done?
