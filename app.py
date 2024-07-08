
from flask import Flask
from userinfo import user_info_bp
from income import user_income_bp
from expance import user_expance_bp
from home import user_home_bp
from adminhome import admin_home_bp


app = Flask(__name__)

# Registering the user_info blueprint under a prefix
app.register_blueprint(user_info_bp, url_prefix='/api')
app.register_blueprint(user_income_bp, url_prefix='/api')
app.register_blueprint(user_expance_bp, url_prefix='/api')
app.register_blueprint(user_home_bp, url_prefix='/api')
app.register_blueprint(admin_home_bp, url_prefix='/api')




if(__name__) == '__main__':
    app.run(debug=True)
