from flask import Flask,render_template,redirect,request,url_for
import random,string,os
from datetime import datetime
import sqlite3
from model import db

db=db()
app=Flask(__name__)



@app.route("/",methods=["POST","GET"])
def home():
    if request.method=="POST":
        urll=request.form.get("url")
        idd=db.add_url(urll)
        return redirect(url_for("home",short_id=idd))
    
    short_id=request.args.get("short_id")
    shorten=None
    if short_id:
        shorten=request.host_url+short_id

    return render_template("index.html",shorten=shorten)

@app.route("/<string:code>")
def redir(code):
    url=db.get_url(code)
    if url:
        return redirect(url)
    else:
        return render_template("error.html")

@app.route("/admin",methods=["GET","POST"])
def admin():
    login=False
    data=None
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        if username=="admin" and password=="ADMINISSAM103":
            login=True
            data=db.get_data
        elif "delete_url" in request.form:
            delete_id=request.form.get("id_delete")
            db.delete_url(delete_id)
            data=db.get_data
            return render_template("admin.html",login=True,data=data,host_url=request.host_url)
    return render_template("admin.html",login=login,data=data,host_url=request.host_url)

if __name__=="__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)