from flask import Flask,jsonify,abort,make_response,request,url_for
from flask_httpauth import HTTPBasicAuth
app = Flask(__name__)

auth = HTTPBasicAuth()
@auth.get_password
def get_password(username):
    if username == 'sseba':
        return 'lawrence'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error':'Unauthorized access'}),401)
tasks = [
    {
        'id': 1,
        'title':u'the first one',
        'description':u'building a restuarant interface',
        'done': False
    },
    {
        'id': 2,
        'title':u'the second one',
        'description':u'building a restuarant interface',
        'done': False
    },
    {
        'id': 3,
        'title':u'the third one',
        'description':u'building a restuarant interface',
        'done': False
    },
    {
        'id': 4,
        'title':u'the forth one',
        'description':u'building a restuarant interface',
        'done': False
    }
    
]
def make_public_task(task):
    new_task = {}

    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task',task_id = task['id'],_external=True)
        else:
            new_task[field] = task[field]
    return new_task
#return all tasks
@app.route('/todo/api/v1.0/tasks',methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks':[make_public_task(task) for task in tasks]})

#return a single task
@app.route('/todo/api/v1.0/tasks/<int:task_id>')
@auth.login_required
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id ]
    if len(task) == 0:
        abort(404)
    return jsonify({'task':make_public_task(task[0])})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}),404)
@app.route('/todo/api/v1.0/tasks',methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title':request.json['title'],
        'description': request.json.get('description',''),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task':make_public_task(task)}),201
@app.route('/todo/api/v1.0/tasks/<int:task_id>',methods=['PUT'])
@auth.login_required
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json('title')) != str:
        abort(400)
    if 'description' in request.json and type(request.json('description')) is not str:
        abort(400)
    # this one is somehow refusing to work    
    # if 'done' in request.json and type(request.json('done')) is not bool:
    #     abort(400)
    
    task[0]['title'] = request.json.get('title',task[0]['title'])
    task[0]['description'] = request.json.get('description',task[0]['description'])
    task[0]['done'] = request.json.get('done',task[0]['done'])

    return jsonify({'task': make_public_task(task[0])})

@app.route('/todo/api/v1.0/tasks/<int:task_id>',methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

@app.route('/')
def index():
    return 'hello world'
if __name__ == "__main__":
    app.run(debug=True,port=2000)
