from flask_bcrypt import generate_password_hash, check_password_hash

def create_user(db, email, password):
    hashed_pw = generate_password_hash(password).decode('utf-8')
    user = {"email": email, "password": hashed_pw}
    db.users.insert_one(user)
    return user

def find_user_by_email(db, email):
    return db.users.find_one({"email": email})

def verify_password(stored_password, provided_password):
    return check_password_hash(stored_password, provided_password)