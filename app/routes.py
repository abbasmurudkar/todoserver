from flask import request, jsonify, current_app as app
from .models import Todo
from . import db

@app.route('/', methods=['POST'])
def add_todo():
    data = request.get_json()
    new_todo = Todo(
        title=data['title'],
        description=data['description'],
        tags=data['tags']
    )
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': 'Todo created successfully'}), 201

@app.route('/', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    todos_list = []
    for todo in todos:
        todos_list.append({
            'id': todo.id,
            'title': todo.title,
            'description': todo.description,
            'tags': todo.tags
        })
    return jsonify(todos_list)

@app.route('/', methods=['DELETE'])
def delete_all_todos():
    try:
        Todo.query.delete()
        db.session.commit()
        return jsonify({'message': 'All Todos Deleted Successfully'}), 200
    except Exception as ex:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete todos', 'error': str(ex)}), 500

@app.route('/<int:id>', methods=['DELETE'])
def delete_particular_todo(id):
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({'message': 'Todo Not Found'}), 400
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo Deleted Successfully'}), 200

@app.route('/<int:id>', methods=['PUT'])
def update_particular_todo(id):
    data = request.get_json()
    todo = Todo.query.get(id)
    if not todo:
        return jsonify({"message": "Todo Not Found"}), 400
    todo.title = data.get("title", todo.title)
    todo.description = data.get("description", todo.description)
    todo.tags = data.get("tags", todo.tags)
    db.session.commit()
    return jsonify({"message": "Todo Updated Successfully"}), 200
