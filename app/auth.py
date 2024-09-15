from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
<<<<<<< HEAD
from app.models import User, db, Investment, Rate
from datetime import datetime

=======
from app.models import User, db
from app.schemas import UserCreateSchema
from flask_jwt_extended import get_jwt
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime


>>>>>>> 6873958458b7c396f826c02bb2bd911cc5fba600
auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

<<<<<<< HEAD
    # Check if the username already exists
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({"msg": "Username already exists"}), 400

    # Check if the referral code is valid
    referrer = None
    if data.get('referrer_code'):
        referrer = User.query.filter_by(code=data.get('referrer_code')).first()
        if not referrer:
            return jsonify({"msg": "Invalid referral code"}), 400

    # Create the new user
    new_user = User(username=data.get('username'))
    new_user.set_password(data.get('password'))
    new_user.referrer = referrer
    db.session.add(new_user)
    db.session.commit()

    # Generate an access token for the new user
    access_token = create_access_token(identity=new_user.id)
=======
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

>>>>>>> 6873958458b7c396f826c02bb2bd911cc5fba600
    return jsonify({"msg": "User created successfully", "access_token": access_token}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
<<<<<<< HEAD
    user = User.query.filter_by(username=data.get('username')).first()

    if user and user.check_password(data.get('password')):
=======
    user_data = UserCreateSchema(**data)

    user = User.query.filter_by(username=user_data.username).first()

    if user and user.check_password(user_data.password):
>>>>>>> 6873958458b7c396f826c02bb2bd911cc5fba600
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Bad username or password"}), 401

<<<<<<< HEAD
# @auth.route('/userinfo', methods=['GET'])
# @jwt_required()
# def userinfo():
#     current_user_id = get_jwt_identity()
#     user = User.query.get(current_user_id)

#     if not user:
#         return jsonify({"msg": "User not found"}), 404

#     # Get referred users with their usernames and IDs
#     referred_users = [{'id': u.id, 'username': u.username} for u in user.referred_users]

#     response = {
#         "username": user.username,
#         "referral_code": user.code,
#         "referred_users": referred_users
#     }
#     return jsonify(response), 200


# @auth.route('/account', methods=['POST'])
# @jwt_required()
# def account():
#     data = request.get_json()
    
#     current_user_id = get_jwt_identity()

#     # Create a new investment with confirm=False, to be confirmed by admin
#     new_investment = Investment(
#         user_id=current_user_id,
#         amount=data.get('amount'),
#         confirm=False,  # Admin will confirm later
#         request_date=datetime.utcnow(),  # Set request date
#         confirm_check_date=None  # Initially None, updated when admin confirms
#     )
    
#     db.session.add(new_investment)
#     db.session.commit()

#     return jsonify({
#         "msg": "Investment request submitted successfully",
#         "investment_id": new_investment.id
#     }), 201

# @auth.route('/accountinfo', methods=['GET'])
# @jwt_required()
# def accountinfo():
#     current_user_id = get_jwt_identity()

#     investments = Investment.query.filter_by(user_id=current_user_id).all()

#     if not investments:
#         return jsonify({"msg": "No investments found for this user"}), 404

#     investments_info = []
    
#     for inv in investments:
#         profit = inv.calculate_profit()
#         active_users_count = inv.get_active_referred_users()

#         applicable_rate = Rate.query.filter(
#             Rate.min_amount <= inv.amount,
#             Rate.min_active_user <= active_users_count
#         ).order_by(Rate.min_amount.desc(), Rate.min_active_user.desc()).first()

#         if not applicable_rate:
#             profit_rate = 0.0
#         else:
#             profit_rate = float(applicable_rate.rate)

#         investments_info.append({
#             "amount": float(inv.amount),
#             "confirm": inv.confirm,
#             "confirm_check_date": inv.confirm_check_date,
#             "profit": float(profit),
#             "profit_rate": profit_rate
#         })

#     return jsonify({
#         "msg": "User account information retrieved successfully",
#         "investments": investments_info
#     }), 200


# @auth.route('/admin/investments', methods=['GET'])
# @jwt_required()
# def admin_investments():
#     current_user_id = get_jwt_identity()
#     user = User.query.get(current_user_id)

#     # Only allow access if the user is an admin
#     if not user.admin:
#         return jsonify({"msg": "Access denied"}), 403

#     # Get all investments that are not confirmed yet
#     pending_investments = Investment.query.filter_by(confirm=False).all()

#     investments_info = []
#     for inv in pending_investments:
#         investments_info.append({
#             "investment_id": inv.id,
#             "username": inv.user.username,
#             "amount": float(inv.amount),
#             "request_date": inv.request_date
#         })

#     return jsonify({
#         "msg": "Pending investments retrieved successfully",
#         "pending_investments": investments_info
#     }), 200
=======

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
>>>>>>> 6873958458b7c396f826c02bb2bd911cc5fba600
