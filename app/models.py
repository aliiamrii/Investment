<<<<<<< HEAD
from datetime import datetime, timedelta
import random
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
=======
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import random
import string

>>>>>>> 6873958458b7c396f826c02bb2bd911cc5fba600

# Initialize SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
<<<<<<< HEAD
    code = db.Column(db.String(40), unique=True, nullable=False, default='')
    referrer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    register_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    admin = db.Column(db.Boolean(), default=False, nullable=False)  # New admin column
    referrer = db.relationship('User', remote_side=[id], backref='referred_users', foreign_keys=[referrer_id])

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        if not self.code:
            self.code = self.generate_unique_referral_code()

    def generate_unique_referral_code(self):
        while True:
            code = str(random.randint(10000, 99999))
            if not self.is_code_exists(code):
                return code

    @staticmethod
    def is_code_exists(code):
        exists = User.query.filter_by(code=code).first() is not None
        return exists

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

=======
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
>>>>>>> 6873958458b7c396f826c02bb2bd911cc5fba600

class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
<<<<<<< HEAD
    amount = db.Column(db.DECIMAL(precision=10, scale=5), nullable=False)
    confirm = db.Column(db.Boolean(), nullable=False, default=False)
    confirm_check_date = db.Column(db.DateTime(), nullable=True)  # Updated by admin confirmation
    profit = db.Column(db.DECIMAL(precision=10, scale=5), nullable=True, default=0.0)
    last_profit_date = db.Column(db.DateTime(), nullable=True)  # Tracks last profit calculation
    request_date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)  # When the request was made

    user = db.relationship('User', backref='investments')

    def calculate_profit(self): 
        if not self.confirm_check_date or not self.confirm:
            return 0.0

        # If last_profit_date is None, set it to the confirm_check_date for the first calculation
        if not self.last_profit_date:
            self.last_profit_date = self.confirm_check_date

        # Ensure confirm_check_date and last_profit_date are datetime objects
        if isinstance(self.confirm_check_date, datetime):
            confirm_check_date = self.confirm_check_date
        else:
            confirm_check_date = datetime.combine(self.confirm_check_date, datetime.min.time())

        if isinstance(self.last_profit_date, datetime):
            last_profit_date = self.last_profit_date
        else:
            last_profit_date = datetime.combine(self.last_profit_date, datetime.min.time())

        current_time = datetime.utcnow()

        # Calculate the number of days since the last profit calculation
        days_since_last_profit = (current_time - last_profit_date).days

        if days_since_last_profit < 1:
            # If less than a day has passed, no new profit should be calculated
            return 0.0

        # Update last_profit_date to the current date
        self.last_profit_date = current_time

        # Calculate the number of days since the confirm_check_date
        days_since_confirm_check = (current_time - confirm_check_date).days

        # Get active users referred by this user
        active_users = self.get_active_referred_users()

        # Query the rate table to get the appropriate rate entry for the current investment
        rate_info = Rate.query.filter(
            Rate.min_amount <= self.amount,
            Rate.min_active_user <= active_users
        ).order_by(Rate.min_amount.desc(), Rate.min_active_user.desc()).first()

        if not rate_info:
            return 0.0

        # Use the rate entry's profit percentage
        profit_percentage = float(rate_info.rate)
        
        # Calculate profit based on days since the confirm_check_date
        profit_amount = days_since_confirm_check * (profit_percentage / 100) * float(self.amount)

        # Round profit amount to 5 decimal places
        profit_amount = round(profit_amount, 5)

        # Update the profit in the database
        self.profit = profit_amount

        # Commit changes to the database
        db.session.commit()

        return profit_amount


    def get_active_referred_users(self):
        #"""Count the number of active users referred by this user."""
        referred_users = User.query.filter_by(referrer_id=self.user_id).all()
        active_users_count = 0
        for user in referred_users:
            total_investment = Investment.get_total_investment_for_user(user.id)
            if total_investment > 0:
                active_users_count += 1
        return active_users_count

    @staticmethod
    def get_total_investment_for_user(user_id):
        """Get the total amount of investments for a specific user."""
        total_investment = db.session.query(func.sum(Investment.amount)).filter_by(user_id=user_id).scalar()
        return total_investment or 0.0


class Rate(db.Model):
    __tablename__ = 'rate'

    id = db.Column(db.Integer, primary_key=True)
    min_amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    min_active_user = db.Column(db.BigInteger, nullable=False)
    rate = db.Column(db.Numeric(precision=5, scale=2), nullable=False)
=======
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
>>>>>>> 6873958458b7c396f826c02bb2bd911cc5fba600
