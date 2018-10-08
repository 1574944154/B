from flask import Flask, request, render_template, redirect, url_for
from account_manage.Account_Manage import AccountManage
from multiprocessing import Process
"""

提供WEB服务

"""


app = Flask(__name__)


@app.route("/admin12", methods=["POST", "GET"])
def index():
    list1 = AccountManage().getall("status")
    list2 = AccountManage().getall("complete")
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        AccountManage().hmset(kname="account", value={username: password})
        return "success"
    return render_template("index.html", list1=list1, list2=list2)

@app.route("/commit")
def commit():
    return render_template("commit.html")

# 接收POST请求的账号密码
@app.route("/receive", methods=["POST"])
def receive():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        AccountManage().hmset(kname="account", value={username: password})
        return redirect(url_for("result", username=username))

# 查询进度的页面
@app.route("/result", methods=["get"])
def result():
    """
    查询状态

    :param num:
    :return:
    """
    num = request.args.get("username")
    code_list = {
        "0b": "您好，客服开始答题，请耐心等待", # 正在登录
        "0": "您好，正在答题，请耐心等待",
        "1b": "您好，正在答题，请耐心等待",
        "1": "您好，正在答题，请耐心等待",
        "2b": "您好，正在答题，请耐心等待",
        "3b": "您好，正在答题，请耐心等待",
        "2": "您好，正在答题，请耐心等待",
        "3": "您好，正在答题，请耐心等待",
        "9": "您好，正在答题，请耐心等待",
        "8": "您好，账号限制12小时内无法答题，请十二小时之后再次提交",
        "7": "您好，账号存在风险，登录不成功，请修改密码再次提交",
        "4": "未绑定手机号无法答题，请先绑定手机号再次提交",
        "4b": "您好，密码错误，请提供正确的密码",
        "5": "您好，正在答题，请耐心等待", #最终验证
	"6b": "您好，正在答题，请耐心等待",
        "6": "答题已经通过哦，您已经是LV1正式会员啦 ✿✿ヽ(ﾟ▽ﾟ)ノ✿"
    }
    status_code = AccountManage().get("status", num)[0]
    if status_code:
        status_code = status_code.decode("utf-8")
        status = code_list[status_code]
        return render_template("result.html", username=num, status=status)
    else:
        return render_template("result.html", username=num, status="尚未开始答题，一般提交账号一分钟内店主开始答题")


# 接收
@app.route("/search", methods=["POST"])
def search():
    username = request.form.get("username")
    return redirect(url_for("result", username=username))

def run():
    print("web start")
    app.run(host="0.0.0.0", port=80)







if __name__ == '__main__':
    p = Process(target=run)
    p.start()
