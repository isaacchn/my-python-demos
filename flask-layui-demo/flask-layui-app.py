from flask import Flask, render_template

app = Flask(__name__)


# 必要时可以通过以下方式修改jinja语法定界符号
# app.jinja_env.block_start_string = '(%'  # 修改块开始符号
# app.jinja_env.block_end_string = '%)'  # 修改块结束符号
# app.jinja_env.variable_start_string = '(('  # 修改变量开始符号
# app.jinja_env.variable_end_string = '))'  # 修改变量结束符号
# app.jinja_env.comment_start_string = '(#'  # 修改注释开始符号
# app.jinja_env.comment_end_string = '#)'  # 修改注释结束符号


@app.route('/')
def index():
    return render_template('index.html', message='Hello World, Flask, Jinja, and Layui.')


if __name__ == '__main__':
    app.run()
