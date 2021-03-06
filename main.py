from flask import Flask, redirect, render_template, request, make_response
from static.module import *

app = Flask(__name__)

box = FillingBox()
cd = None # global card for the learn() and know() function

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods = ['POST', 'GET'])
def add():
    flag = False
    flag2 = False
    if request.method == "POST":
        front = request.form["front"]
        back = request.form["back"]

        # check for empty inputs 
        if len(front) > 1 and len(back) > 1:
            card = Card(front, back)
            try:
                box.add_card(card)
            except:
                flag = True
        else:
            flag2 = True
        return render_template("add.html", status = flag, status2 = flag2)
    else:
        return render_template("add.html", status = flag)

@app.route("/display")
def display():
    flag = box.is_empty()
    return render_template("display.html", data = box.get_compartments(), status = flag)

@app.route("/remove", methods = ["POST", "GET"])
def remove():
    flag = False
    if request.method == "POST":
        front = request.form["front"]
        back = request.form["back"]
        deck = int(request.form["deck"]) -1
        try:
            box.remove(deck, Card(front, back))
        except:
            flag = True
        return render_template("remove.html", status = flag)
    else:
        return render_template("remove.html")

@app.route("/learn", methods = ["POST", "GET"])
def learn():
    global cd
    data = ""
    flag = False
    if request.method == "POST":
        deck = int(request.form["deck"]) -1
        box.select(deck)
        try:
            cd = box.learn()
        except:
            return render_template("learn.html", word = data, status = True, status2 = False)
        if cd == None:
            data = ""
            flag = True
        else:
            data = cd.get_front()
        return render_template("learn.html", word = data, status = flag, status2 = False)
    else:
        return render_template("learn.html", word = data, status = flag, status2 = False)

@app.route("/learn/know", methods = ["POST", "GET"])
def know():
    flag = False
    if request.method == "POST":
        if cd == None:
            flag = True
        else:
            box.is_known(cd)
        return render_template("learn.html", word = "", status = False, status2 = flag)
    else:
        return render_template("learn.html", word = "", status = False, status2 = flag)

@app.route("/io")
def io():
    return render_template("io.html")

@app.route("/io/save", methods = ["POST", "GET"])
def save():
    response = make_response(box.create_CSV())
    response.headers['Content-Disposition'] = 'attachment; filename=words.csv'
    response.mimetype='text/csv'
    return response

@app.route("/io/load", methods = ["POST", "GET"])
def load():
    if request.method == "POST":
        path = request.form["file"]
        box.load(path)
    
    return render_template("io.html")

@app.route("/edit", methods = ["POST", "GET"])
def edit():
    flag = False
    if request.method == "POST":
        deck = int(request.form["deck"]) -1
        com = box.get_compartments()[deck]
        flag = True
        if "front" in request.form:
            if len(request.form["front"]) > 0 and len(request.form["back"]) > 0:
                id = int(request.form["card"]) -1
                com = box.get_compartments()[deck]
                cs = com.get_cards()
                cs[id].set_front(request.form["front"])
                cs[id].set_back(request.form["back"])
        return render_template("edit.html", cards = com.get_cards(), status = flag)
    else:
        return render_template("edit.html", status = flag)

if __name__ == "__main__":
    app.run()
    # app.run(debug = True)