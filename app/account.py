from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, db, Investment, Rate
from datetime import datetime

account = Blueprint('account', __name__)

@account.route('/accountinfo', methods=['GET'])
@jwt_required()
def accountinfo():
    current_user_id = get_jwt_identity()
    investments = Investment.query.filter_by(user_id=current_user_id).all()

    if not investments:
        return jsonify({"msg": "No investments found for this user"}), 404

    investments_info = []
    
    for inv in investments:
        profit = inv.calculate_profit()
        active_users_count = inv.get_active_referred_users()

        applicable_rate = Rate.query.filter(
            Rate.min_amount <= inv.amount,
            Rate.min_active_user <= active_users_count
        ).order_by(Rate.min_amount.desc(), Rate.min_active_user.desc()).first()

        profit_rate = float(applicable_rate.rate) if applicable_rate else 0.0

        investments_info.append({
            "amount": float(inv.amount),
            "confirm": inv.confirm,
            "confirm_check_date": inv.confirm_check_date,
            "profit": float(profit),
            "profit_rate": profit_rate
        })

    return jsonify({
        "msg": "User account information retrieved successfully",
        "investments": investments_info
    }), 200

@account.route('/admin/investments', methods=['GET'])
@jwt_required()
def admin_investments():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Only allow access if the user is an admin
    if not user.admin:
        return jsonify({"msg": "Access denied"}), 403

    # Get all investments that are not confirmed yet
    pending_investments = Investment.query.filter_by(confirm=False).all()

    investments_info = []
    for inv in pending_investments:
        investments_info.append({
            "investment_id": inv.id,
            "username": inv.user.username,
            "amount": float(inv.amount),
            "request_date": inv.request_date
        })

    return jsonify({
        "msg": "Pending investments retrieved successfully",
        "pending_investments": investments_info
    }), 200
