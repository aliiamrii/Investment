from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Investment, db
from datetime import datetime
from app.models import User


investment = Blueprint('investment', __name__)

@investment.route('/create', methods=['POST'])
@jwt_required()
def create_investment():
    data = request.get_json()
    amount = data.get('amount')

    if not amount or amount <= 0:
        return jsonify({"msg": "Invalid investment amount"}), 400

    current_user_id = get_jwt_identity()
    new_investment = Investment(user_id=current_user_id, amount=amount)
    db.session.add(new_investment)
    db.session.commit()

    return jsonify({"msg": "Investment created successfully", "investment_id": new_investment.id}), 201


# @investment.route('/admin/confirm/<int:investment_id>', methods=['POST'])
# @jwt_required()
# @admin_required()  # You would need to implement this decorator to restrict access to admins
# def admin_confirm_investment(investment_id):
#     # Admin-only route to confirm an investment
#     investment = Investment.query.get(investment_id)

#     if not investment:
#         return jsonify({"msg": "Investment not found"}), 404

#     if investment.is_confirmed:
#         return jsonify({"msg": "Investment already confirmed"}), 400

#     # Confirm the investment
#     investment.is_confirmed = True
#     db.session.commit()

#     return jsonify({"msg": "Investment confirmed successfully"}), 200

@investment.route('/profit', methods=['GET'])
@jwt_required()
def get_total_profit():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Fetch all confirmed investments for the current user
    confirmed_investments = Investment.query.filter_by(user_id=current_user_id, is_confirmed=True).all()

    if not confirmed_investments:
        return jsonify({"msg": "No confirmed investments found"}), 404

    total_profit = 0
    total_amount = 0
    unique_dates = set()

    # Calculate user's level based on the database
    level = user.calculate_level()

    if not level:
        return jsonify({"msg": "Unable to calculate level"}), 400

    # Get the profit multiplier for the user's level
    profit_multiplier = level.profit_multiplier

    # Loop through investments and calculate profit
    for investment in confirmed_investments:
        result = investment.get_profit()
        # Adjust the profit based on the user's level
        total_profit += result['profit'] * profit_multiplier
        total_amount += result['amount']
        unique_dates.add(investment.start_time.date())  # Ensure unique days

    # Calculate total days active based on unique dates
    today = datetime.now().date()
    total_days_active = sum((today - date).days for date in unique_dates)

    return jsonify({
        "total_amount": total_amount,
        "total_profit": total_profit,
        "total_investments": len(confirmed_investments),
        "total_days_active": total_days_active,
        "user_level": level.id,
        "profit_multiplier": profit_multiplier
    }), 200
