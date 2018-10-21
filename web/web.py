from flask import Flask, request, render_template, redirect, url_for
from account_manage.Account_Manage import AccountDB
from multiprocessing import Process
import json
"""

提供WEB服务

"""


app = Flask(__name__)
conn = AccountDB()

@app.route("/admin")
def admin():
    list1 = conn.hgetall("complete")
    return render_template("manage.html", list1=list1, list2=list1)

@app.route("/commit")
def commit():
    return render_template("commit.html")

@app.route("/search", methods=['POST', 'GET'])
def search():
    username = request.form.get("username")
    return redirect(url_for("result", username=username))

@app.route("/receive", methods=["POST"])
def receive():
    username = request.form.get("username").strip()
    password = request.form.get("password").strip()
    conn.hmset("history", {username+":"+password:password}) # 保存post记录
    result = conn.hmget("status:"+username, "status")[0]
    if result:
        if (result == "7") or (result == "8") or (result == "4b"):
            conn.rpush("account", {"username": username, "password": password})
            return redirect(url_for("result", username=username))
        else:
            return redirect(url_for("result", username=username))
    else:
        conn.rpush("account", {"username": username, "password": password})
    return redirect(url_for("result", username=username))

@app.route("/result")
def result():
    username = request.args.get("username")
    result = conn.hmget("status:"+username, "status")[0]
    type = conn.hmget("status:"+username, "type")[0]
    type_text = ""
    if type:

        if type == "1":
            type_text = "会员转正答题"
        elif type == "2":
            type_text = "小黑屋答题"
    if result:
        status_code = result
        code_list = {
            "-1": "您好，客服开始答题，请耐心等待",
            "0b": "您好，客服开始答题，请耐心等待",  # 正在登录
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
            "5": "您好，正在答题，请耐心等待",  # 最终验证
            "6b": "您好，正在答题，请耐心等待",
            "6": "答题已经通过哦，您已经是LV1正式会员啦 ✿✿ヽ(ﾟ▽ﾟ)ノ✿",
            "10": "答题已经通过哦，封禁时间到后即可解封"
        }
        status = code_list[status_code]
        return render_template("result.html", username=username, type=type_text, status=status)
    else:
        return render_template("result.html", username=username, type=type_text, status="尚未开始答题")



@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

def run():
    print("web start")
    app.run(host="0.0.0.0", port=80)


if __name__ == '__main__':
    p = Process(target=run)
    p.start()
