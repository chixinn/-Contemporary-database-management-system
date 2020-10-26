from flask import Flask, jsonify, request, abort,url_for,render_template,redirect
from time import time
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'todolist'

app.config['MONGO_URI'] = 'mongodb://todo:towait.com@localhost:27017/todolist'

app.url_map.strict_slashes = False

mongo = PyMongo(app)


@app.route("/", methods=['GET'])
def home_page():
    return "<h1>Hello World!</h1>"


class Todo(object):
    @classmethod
    def create_doc(cls, content):
        return {
            'content': content,
            'created_at': time(),
            'is_finished': False,
            'finished_at': None
        }

@app.route('/todo/',methods=['GET'])
def index():
    todos = mongo.db.todos.find({})
    return  render_template('index.html',todos=todos)

@app.route('/todo/', methods=['POST'])
def add():
    content = request.form.get('content', None)
    if not content:
        abort(400)
    mongo.db.todos.insert(Todo.create_doc(content))
    return redirect('/todo/')

@app.route('/todo/<content>/finished')
def finish(content):
    result = mongo.db.todos.update_one(
        {'content':content},
        {
            '$set': {
                'is_finished': True,
                'finished_at': time()
            }
        }    
    )
    return redirect('/todo/')

@app.route('/todo/<content>')
def delete(content):
    result = mongo.db.todos.delete_one(
        {'content':content}
    )
    return redirect('/todo/')

@app.route('/todo/search/<content>')
def find(content):
    todos = mongo.db.todos.find(
        {'content': {"$regex": content}} 
    )
    return  render_template('index.html', todos=todos)

if __name__ == '__main__':
    app.run(debug=True)
