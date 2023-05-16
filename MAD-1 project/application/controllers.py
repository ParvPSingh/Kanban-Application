from flask import render_template, request, redirect, url_for
from flask import current_app as app
from application.models import User, List, Card, Summary
from application.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter


@app.route("/", methods=["GET","POST"])
def signup():
    if request.method=="GET":
        return render_template("signup.html")
    elif request.method=="POST":
        username=request.form.get("username")
        now_user=User.query.filter_by(user_name=username).first()
        password=request.form.get("password")
        confirm_password=request.form.get("confirm_password")
        if now_user:
            notuser=True
            return render_template("signup.html", notuser=notuser)
        elif len(password)<7:
            notlen=True
            return render_template("signup.html", notlen=notlen)
        elif password.islower()==True:
            notup=True
            return render_template("signup.html", notup=notup)
        elif str(password)!=str(confirm_password):
            notequal=True
            return render_template("signup.html", notequal=notequal)
        else:
            new_user=User(user_name=username, password=generate_password_hash(password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
        return redirect(url_for("login_page"))
    else:
        return render_template("error.html", user=username)                          

@app.route("/login", methods=["GET","POST"])
def login_page():
    if request.method=="GET":
        return render_template("login.html")
    elif request.method=="POST":          
        username=request.form.get("username")
        password=request.form.get("password")
        now_user=User.query.filter_by(user_name=username).first()
        if now_user:
            if check_password_hash(now_user.password, password):
                return redirect(url_for("index", user=username))
            else:
                notpass=True
                return render_template("login.html", notpass=notpass)
        else:
            notuser=True
            return render_template("login.html", notuser=notuser)
    else:
        return render_template("error.html", user=username)

@app.route("/index/<user>", methods=["GET"])
def index(user):
    if request.method=="GET":
        now_user=User.query.filter_by(user_name=user).first()
        lists=List.query.filter_by(list_user_id=now_user.user_id).all()
        listcards={}
        if lists:
            for i in lists:
                cards=Card.query.filter_by(card_list_id=i.list_id).all()
                if cards:
                    listcards[i.list_id]=cards

        return render_template("index.html", user=user, lists=lists, listcards=listcards)
    else:
        return render_template("error.html", user=user)

@app.route("/add_list/<user>", methods=["GET","POST"])
def add_list(user):
    if request.method=="GET":
        return render_template("add_list.html", user=user)
    elif request.method=="POST":
        now_user=User.query.filter_by(user_name=user).first()
        title=request.form.get("listTitle")
        description=request.form.get("listDescription")
        if title=="":
            notitle=True
            return render_template("add_list.html", user=user, notitle=notitle)
        else:
            new_list=List(list_title=title, list_description=description, list_user_id=now_user.user_id)
            db.session.add(new_list)
            db.session.commit()
            return redirect(url_for("index", user=user))
    else:
        return render_template("error.html", user=user)

@app.route("/update_list/<user>/<int:list_id>", methods=["GET","POST"])
def update_list(user, list_id):
    if request.method=="GET":
        return render_template("update_list.html", user=user)
    elif request.method=="POST":
        now_list=List.query.filter_by(list_id=list_id).first()
        title=request.form.get("list-Title")
        description=request.form.get("list-Description")
        if title=="":
            notitle=True
            return render_template("add_list.html", user=user, notitle=notitle)
        else:
            now_list.list_title=title
            now_list.list_description=description
            db.session.commit()
            return redirect(url_for("index", user=user))
    else:
        return render_template("error.html", user=user)

@app.route("/delete_list/<user>/<int:list_id>", methods=["GET"])
def delete_list(user, list_id):
    if request.method=="GET":
        now_list=List.query.filter_by(list_id=list_id).first()
        db.session.delete(now_list)
        db.session.commit()
        return redirect(url_for("index", user=user))
    else:
        return render_template("error.html", user=user)

@app.route("/add_card/<user>/<int:list_id>", methods=["GET","POST"])
def add_card(user, list_id):
    if request.method=="GET":
        lists=List.query.filter_by(list_id=list_id).first()
        return render_template("add_card.html", user=user, lists=lists)
    elif request.method=="POST":
        lists=List.query.filter_by(list_id=list_id).first()
        select_list_id=request.form.get("list_titles")
        title=request.form.get("cardTitle")
        if title=="":
            notitle=True
            return render_template("add_card.html", user=user, lists=lists, notitle=notitle)
        content=request.form.get("cardContent")
        create_date=datetime.today()
        deadline=request.form.get("Deadline")
        if deadline=="":
            nodeadline=True
            return render_template("add_card.html", user=user, lists=lists, nodeadline=nodeadline)
        date_object = datetime.strptime(deadline, '%Y-%m-%d')
        done=request.form.get("Complete")
        if done=="on":
            today = datetime.today()
            done_date=today
        else:
            done_date=None
        new_card=Card(card_title=title, card_content=content, card_create_date=create_date, card_done=done, card_deadline=date_object, card_done_date=done_date, card_list_id=select_list_id)
        db.session.add(new_card)
        db.session.commit()
        return redirect(url_for("index", user=user))
    else:
        return render_template("error.html", user=user)

@app.route("/update_card/<user>/<int:card_id>", methods=["GET","POST"])
def update_card(user, card_id):
    if request.method=="GET":
        now_user=User.query.filter_by(user_name=user).first()
        lists=List.query.filter_by(list_user_id=now_user.user_id).all()
        return render_template("update_card.html", user=user, lists=lists)
    elif request.method=="POST":
        now_user=User.query.filter_by(user_name=user).first()
        lists=List.query.filter_by(list_user_id=now_user.user_id).all()
        select_list_id=request.form.get("list_titles")
        if select_list_id=="Select List To Insert Card":
            no_select_list=True
            return render_template("update_card.html", user=user, lists=lists, no_select_list=no_select_list)
        title=request.form.get("cardTitle")
        if title=="":
            notitle=True
            return render_template("update_card.html", user=user, lists=lists, notitle=notitle)
        content=request.form.get("cardContent")
        deadline=request.form.get("Deadline")
        if deadline=="":
            nodeadline=True
            return render_template("update_card.html", user=user, lists=lists, nodeadline=nodeadline)
        date_object = datetime.strptime(deadline, '%Y-%m-%d')
        print(date_object)
        print(type(date_object))
        done=request.form.get("Complete")
        if done=="on":
            today = datetime.today()
            done_date=today
        else:
            done_date=None
        now_card=Card.query.filter_by(card_id=card_id).first()
        now_card.card_list_id=select_list_id
        now_card.card_title=title
        now_card.card_content=content
        now_card.card_deadline=date_object
        now_card.card_done=done
        now_card.card_done_date=done_date
        db.session.commit()
        return redirect(url_for("index", user=user))
    else:
        return render_template("error.html", user=user)

@app.route("/delete_card/<user>/<int:card_id>", methods=["GET"])
def delete_card(user, card_id):
    if request.method=="GET":
        now_card=Card.query.filter_by(card_id=card_id).first()
        db.session.delete(now_card)
        db.session.commit()
        return redirect(url_for("index", user=user))
    else:
        return render_template("error.html", user=user)

@app.route("/summary/<user>", methods=["GET","POST"])
def summary(user):
    if request.method=="GET":
        now_user=User.query.filter_by(user_name=user).first()
        lists=List.query.filter_by(list_user_id=now_user.user_id).all()
        len_of_total_cards_in_list={}
        len_of_done_cards_in_list={}
        len_of_passed_deadline_cards_in_list={}

        if lists:
            for i in lists:
                cards=Card.query.filter_by(card_list_id=i.list_id).all()
                if cards:
                    len_of_total_cards_in_list[i.list_id]=len(cards)
                no_of_done_cards=0
                for x in cards:
                    if x.card_done=="on":
                        no_of_done_cards+=1
                len_of_done_cards_in_list[i.list_id]=no_of_done_cards
                no_of_passed_deadline_cards=0
                for y in cards:
                    if y.card_done_date:
                        if y.card_done_date>y.card_deadline:
                            no_of_passed_deadline_cards+=1
                len_of_passed_deadline_cards_in_list[i.list_id]=no_of_passed_deadline_cards
                graphs=False
                if cards:
                    datesDone=[]
                    datesNotDone=[]
                    for j in cards:
                        if j.card_done is None:
                            datesNotDone.append(str(j.card_create_date.date()))
                        else:
                            datesDone.append(str(j.card_create_date.date()))
                    create_date_dict=Counter(datesDone)
                    plt.rcParams.update({'font.size': 22})
                    namesDone=list(create_date_dict.keys())
                    valuesDone=list(create_date_dict.values())
                    fig = plt.figure(figsize = (10, 5))
                    plt.bar(namesDone, valuesDone, color=(0.6, 0.8, 0.4, 0.6))
                    print(namesDone)
                    print(valuesDone)
                    #plt.xlabel('Creation Dates')
                    plt.ylabel('Complete Tasks')
                    plt.title("Creation dates and their complete tasks")
                    plt.savefig("static/graph_"+str(i.list_id)+"_done.png")

                    create_not_date_dict=Counter(datesNotDone)
                    namesNotDone=list(create_not_date_dict.keys())
                    valuesNotDone=list(create_not_date_dict.values())
                    fig = plt.figure(figsize = (10, 5))
                    plt.bar(namesNotDone, valuesNotDone, color=(1.0, 0, 0, 0.6))
                    #plt.xlabel('Creation Dates')
                    plt.ylabel('Incomplete Tasks')
                    plt.title("Creation dates and their incomplete tasks")
                    plt.savefig("static/graph_"+str(i.list_id)+"_not_done.png")
                    graphs=True
                else:
                    graphs=False

                new_summary=Summary(sum_cards_total=len(cards), sum_cards_done=no_of_done_cards, sum_cards_deadline=no_of_passed_deadline_cards, sum_graphs=graphs, sum_list_id=i.list_id)
                db.session.add(new_summary)
                db.session.commit()
        return render_template("summary.html", user=user, lists=lists, len_of_total_cards_in_list=len_of_total_cards_in_list, len_of_done_cards_in_list=len_of_done_cards_in_list, len_of_passed_deadline_cards_in_list=len_of_passed_deadline_cards_in_list)
    else:
        return render_template("error.html", user=user)
