from application.database import db

class User(db.Model):
    __tablename__="User"
    user_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name=db.Column(db.String(25), unique=True, nullable=False)
    password=db.Column(db.String(25), unique=True, nullable=False)
    lists=db.relationship("List", backref="user", lazy=True)

class List(db.Model):
    __tablename__="List"
    list_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    list_title=db.Column(db.String(25), nullable=False)
    list_description=db.Column(db.String(125))
    list_user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'),nullable=False)
    cards=db.relationship("Card", backref="list", cascade="all, delete", lazy=True)
    sums=db.relationship("Summary", backref="list", cascade="all, delete", lazy=True)

class Card(db.Model):
    __tablename__="Card"
    card_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    card_title=db.Column(db.String(25), nullable=False)
    card_content=db.Column(db.String(125))
    card_create_date=db.Column(db.DateTime, nullable=False)
    card_deadline=db.Column(db.DateTime, nullable=False)
    card_done=db.Column(db.String(4))
    card_done_date=db.Column(db.DateTime)
    card_list_id = db.Column(db.Integer, db.ForeignKey('List.list_id'),nullable=False)

class Summary(db.Model):
    __tablename__="Summary"
    sum_id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    sum_cards_total=db.Column(db.Integer)
    sum_cards_done=db.Column(db.Integer)
    sum_cards_deadline=db.Column(db.Integer)
    sum_graphs=db.Column(db.Boolean)
    sum_list_id = db.Column(db.Integer, db.ForeignKey('List.list_id'),nullable=False)