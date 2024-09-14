from flask_sqlalchemy import SQLAlchemy
import bcrypt
import random
import string


# Initialize SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    referral_code = db.Column(db.String(50), unique=True, nullable=True)
    referred_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    # referred_users = db.Column(MutableList.as_mutable(ARRAY(db.Integer)), default=[])
    
    referrer = db.relationship('User', remote_side=[id], backref='referred_users_rel')


    def set_password(self, password: str):
        """Hash the password and store the hash."""
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the stored hash."""
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())
    
    def generate_referral_code(self):
        """Generate a unique referral code."""
        while True:
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            if not User.query.filter_by(referral_code=code).first():
                self.referral_code = code
                break

    def get_active_referred_users(self):
        """Return the number of active referred users (with at least one confirmed investment)."""
        active_users = 0
        for referred_user in self.referred_users_rel:
            confirmed_investments = Investment.query.filter_by(user_id=referred_user.id, is_confirmed=True).count()
            if confirmed_investments > 0:
                active_users += 1
        return active_users

    def calculate_level(self):
        """Calculate the user's level based on active referred users and their total investment."""
        active_users = self.get_active_referred_users()

        # Calculate the total amount invested by the user
        total_investment = sum([investment.amount for investment in self.investments if investment.is_confirmed])

        # Fetch the highest level the user qualifies for based on active users and total investment
        level = Level.query.filter(
            Level.min_active_users <= active_users,
            Level.min_amount <= total_investment
        ).order_by(Level.id.desc()).first()

        return level if level else None


from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    is_confirmed = db.Column(db.Boolean, default=False)
    last_withdraw_time = db.Column(db.DateTime, default=None)  # Track the last withdrawal time
    cycle_length = db.Column(db.Integer, default=30)  # Profit cycle length in days (30 days)

    # Relationship to link Investment to User
    user = db.relationship('User', backref='investments')

    def get_profit(self):
        if not self.is_confirmed:
            return {"msg": "Investment not confirmed"}, 400

        # Calculate the number of days since the investment was confirmed
        current_time = datetime.utcnow()
        days_active = (current_time - self.start_time).days

        if days_active < 0:
            return {"msg": "Invalid start time"}, 400

        # Ensure at least one full cycle (30 days) is complete
        if self.last_withdraw_time:
            days_since_last_withdrawal = (current_time - self.last_withdraw_time).days
            if days_since_last_withdrawal < self.cycle_length:
                return {"msg": f"Cannot withdraw profit yet. {self.cycle_length}-day cycle not complete."}, 400
        else:
            # If it's the first withdrawal, ensure at least one full cycle is complete
            if days_active < self.cycle_length:
                return {"msg": f"Cannot withdraw profit yet. {self.cycle_length}-day cycle not complete."}, 400

        # Daily interest rate (0.1% per day)
        daily_rate = 0.001

        # Calculate completed cycles (e.g., how many full 30-day periods have passed)
        completed_cycles = days_active // self.cycle_length

        # Calculate profit based on the number of completed cycles
        profit = self.amount * ((1 + daily_rate) ** (completed_cycles * self.cycle_length) - 1)

        return {
            "amount": self.amount,
            "profit": profit,
            "completed_cycles": completed_cycles,
            "days_active": days_active
        }

    def withdraw_profit(self):
        """Withdraw profit and reset the last withdrawal time."""
        current_time = datetime.utcnow()

        # Check if the 30-day cycle has been completed
        days_active = (current_time - self.start_time).days
        if days_active < self.cycle_length:
            return {"msg": "Profit cycle not complete. Cannot withdraw yet."}, 400

        # Update the last withdrawal time
        self.last_withdraw_time = current_time
        db.session.commit()

        return {"msg": "Profit successfully withdrawn", "withdrawal_time": current_time}




class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    min_active_users = db.Column(db.Integer, nullable=False)
    min_amount = db.Column(db.Float, nullable=False)
    profit_multiplier = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Level {self.id}>"