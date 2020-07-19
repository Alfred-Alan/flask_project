
from app import *

import user_view
import get_order
import add_order
app.register_blueprint(user_view.user)
app.register_blueprint(get_order.orders)
app.register_blueprint(add_order.order)

@app.route('/',methods=['GET','POST'])
def index():
    return '12345'

# /get_file/61b7dbb7-6d69-4a0f-81c6-a1a2f05110c3.png
# 展示本地图片路由
@app.route('/get_file/<file_name>', methods=['GET'])
def get_file(file_name):
    try:
        response = make_response(
            send_from_directory('./static/', file_name, as_attachment=True))
        return response
    except Exception as e:
        return f"文件读取异常{e}"

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)