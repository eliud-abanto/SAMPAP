from app import app
#from utils.db import db
from models.user import User
from utils.init_db import create_user_default

with app.app_context():
  #db.create_all()
  if not User.query.filter_by(username='defaultadmin').first():
    create_user_default()

if __name__ == '__main__':
  app.run(debug=True)

