
from app import *

import user_view
app.register_blueprint(user_view.user)

@app.route('/',methods=['GET','POST'])
def index():

    return '12345'




if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)