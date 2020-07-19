
from app import *
import user_view
import nummber_register
app.register_blueprint(user_view.user)
app.register_blueprint(nummber_register.number)





if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)