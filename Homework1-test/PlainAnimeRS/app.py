# File Name: app.py

from flask import Flask, render_template, request

# 从 recommand.py 文件中引入同名函数
from recommand import recommand


# 创建 Flask Web 应用
app = Flask(__name__)


# 首页视图函数
@app.route('/')
def index():
    return render_template('index.html')

# 搜索页视图函数
@app.route('/search')
def search():
    # 从 request.args 字典中获取用户 ID
    user_id = request.args.get('user_id')
    # 调用 recommand 函数获取推荐数据
    data = recommand(user_id)
    return render_template('search.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
