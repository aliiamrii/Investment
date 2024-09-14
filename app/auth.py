from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User, db
from app.schemas import UserCreateSchema
from flask_jwt_extended import get_jwt
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime


auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate only username and password with UserCreateSchema
    validated_data = UserCreateSchema(**data)

    username = validated_data.username
    password = validated_data.password
    referral_code = data.get('referral_code')  # Extract referral code separately

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400

    # Check if referral code exists and is valid
    referrer = None
    if referral_code:
        referrer = User.query.filter_by(referral_code=referral_code).first()
        if not referrer:
            return jsonify({"msg": "Invalid referral code"}), 400

    new_user = User(username=username)
    new_user.set_password(password)
    new_user.generate_referral_code()

    # If referral code is valid, link new user to referrer
    if referrer:
        new_user.referred_by = referrer.id

    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id)

    return jsonify({"msg": "User created successfully", "access_token": access_token}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_data = UserCreateSchema(**data)

    user = User.query.filter_by(username=user_data.username).first()

    if user and user.check_password(user_data.password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Bad username or password"}), 401


@auth.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Use referred_users_rel to get users referred by the current user
    referred_users = [{'id': u.id, 'username': u.username} for u in user.referred_users_rel] if user.referred_users_rel else []

    response = {
        "username": user.username,
        "referral_code": user.referral_code,
        "referred_users": referred_users
    }
    return jsonify({"msg":"Login successfully","access_token":response}), 200




@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    
    # Get the JWT data
    token_data = get_jwt()
    
    # Extract the 'exp' field from the token and convert it to a human-readable format
    expiration_timestamp = token_data['exp']
    expiration_datetime = datetime.utcfromtimestamp(expiration_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
    return jsonify({
        "logged_in_as": current_user_id,
        "expires_at": expiration_datetime
    }), 200