from datetime import datetime
from app import db, bcrypt
from app import login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key= True)
    user_name = db.Column(db.String(20))
    user_last_name = db.Column(db.String(30))
    user_email = db.Column(db.String(60), unique= True, index= True)
    user_password = db.Column(db.String(80))
    profile_picture = db.Column(db.String(120), nullable=True)
    create_date = db.Column(db.DateTime, default = datetime.now)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.user_password, password)
    
    @classmethod
    def create_user(cls, name, last_name, email, password, profile_picture):
        user = cls(
            user_name       = name, 
            user_last_name  = last_name, 
            user_email      = email,
            user_password   = bcrypt.generate_password_hash(password).decode("utf-8"),
            profile_picture = profile_picture
        )

        db.session.add(user)
        db.session.commit()
        return user
    
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

