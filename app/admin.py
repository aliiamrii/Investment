from flask import Blueprint, request, jsonify
from app.models import Level, db

admin = Blueprint('admin', __name__)

@admin.route('/levels', methods=['GET'])
def get_levels():
    levels = Level.query.all()
    return jsonify([{
        "id": level.id,
        "min_active_users": level.min_active_users,
        "min_amount": level.min_amount,
        "profit_multiplier": level.profit_multiplier
    } for level in levels])

@admin.route('/levels', methods=['POST'])
def create_level():
    data = request.get_json()
    new_level = Level(
        min_active_users=data['min_active_users'],
        min_amount=data['min_amount'],
        profit_multiplier=data['profit_multiplier']
    )
    db.session.add(new_level)
    db.session.commit()
    return jsonify({"msg": "Level created", "level_id": new_level.id}), 201
