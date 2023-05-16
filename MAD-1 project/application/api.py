from flask_restful import Resource, fields, marshal_with, reqparse
from application.database import db
from application.models import Summary, User, List, Card
from application.validation import ValidationError
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

user_out_fields={"user_id": fields.Integer, "user_name": fields.String, "password": fields.String}
list_out_fields={"list_id": fields.Integer, "list_title": fields.String, "list_description": fields.String, "list_user_id": fields.Integer}
card_out_fields={"card_id": fields.Integer, "card_title": fields.String, "card_content": fields.String, "card_create_date": fields.DateTime, "card_deadline": fields.DateTime, "card_done": fields.String, "card_done_date": fields.DateTime, "card_list_id": fields.Integer}
sum_out_fields={"sum_id": fields.Integer, "sum_cards_total": fields.Integer, "sum_cards_done":fields.Integer, "sum_cards_deadline": fields.Integer, "sum_graphs": fields.Boolean, "sum_list_id": fields.Integer}

create_user_parser=reqparse.RequestParser()
create_user_parser.add_argument("user_id")
create_user_parser.add_argument("user_name")
create_user_parser.add_argument("password")

create_list_parser=reqparse.RequestParser()
create_list_parser.add_argument("list_id")
create_list_parser.add_argument("list_title")
create_list_parser.add_argument("list_description")
create_list_parser.add_argument("list_user_id")
update_list_parser=reqparse.RequestParser()
update_list_parser.add_argument("list_title")
update_list_parser.add_argument("list_description")

create_card_parser=reqparse.RequestParser()
create_card_parser.add_argument("card_id")
create_card_parser.add_argument("card_title")
create_card_parser.add_argument("card_content")
create_card_parser.add_argument("card_deadline")
create_card_parser.add_argument("card_done")
create_card_parser.add_argument("card_list_id")
update_card_parser=reqparse.RequestParser()
update_card_parser.add_argument("card_title")
update_card_parser.add_argument("card_content")
update_card_parser.add_argument("card_deadline")
update_card_parser.add_argument("card_done")
update_card_parser.add_argument("card_list_id")

create_sum_parser=reqparse.RequestParser()
create_sum_parser.add_argument("sum_id")

class UserAPI(Resource):
    @marshal_with(user_out_fields)
    def get(self, username):
        now_user=User.query.filter_by(user_name=username).first()
        if now_user:
            return now_user, 201
        else:
            raise ValidationError(status_code=404, error_code="UVE1001", error_message="user doesn't exist")

    @marshal_with(user_out_fields)
    def post(self):
        args=create_user_parser.parse_args()
        user_name=args.get("user_name", None)
        password=args.get("password",None)

        if user_name is None:
            raise ValidationError(status_code=400, error_code="UVE1002", error_message="username is required")
        if password is None:
            raise ValidationError(status_code=400, error_code="UVE1003", error_message="password is required")
        
        now_user_name=User.query.filter_by(user_name=user_name).first()
        if now_user_name:
            raise ValidationError(status_code=400, error_code="UVE1004", error_message="duplicate username")
        
        new_user=User(user_name=user_name, password=generate_password_hash(password, method="sha256"))
        db.session.add(new_user)
        db.session.commit()

        return new_user, 201

class ListAPI(Resource):
    @marshal_with(list_out_fields)
    def get(self, list_id):
        now_list=List.query.filter_by(list_id=list_id).first()
        if now_list:
            return now_list, 201
        else:
            raise ValidationError(status_code=404, error_code="LVE1001", error_message="list doesn't exist")

    @marshal_with(list_out_fields)
    def post(self):
        args=create_list_parser.parse_args()
        list_title=args.get("list_title", None)
        list_description=args.get("list_description", None)
        list_user_id=args.get("list_user_id", None)

        if list_title is None:
            raise ValidationError(status_code=400, error_code="LVE1002", error_message="list title is required")
        if list_user_id is None:
            raise ValidationError(status_code=400, error_code="LVE1003", error_message="list user_id is required")

        new_list=List(list_title=list_title, list_description=list_description, list_user_id=list_user_id)
        db.session.add(new_list)
        db.session.commit()

        return new_list, 201

    @marshal_with(list_out_fields)
    def put(self, list_id):
        args=update_list_parser.parse_args()
        list_title=args.get("list_title", None)
        list_description=args.get("list_description", None)

        if list_title is None:
            raise ValidationError(status_code=400, error_code="LVE1002", error_message="list title is required")

        new_list=List.query.filter_by(list_id=list_id).first()
        new_list.list_title=list_title
        new_list.list_description=list_description
        db.session.commit()

        return new_list, 201

    def delete(self, list_id):
        now_list=List.query.filter_by(list_id=list_id).first()
        if now_list is None:
            raise ValidationError(status_code=404, error_code="LVE1001", error_message="list doesn't exist")
        db.session.delete(now_list)
        db.session.commit()
        return "", 200

class CardAPI(Resource):
    @marshal_with(card_out_fields)
    def get(self, card_id):
        now_card=Card.query.filter_by(card_id=card_id).first()
        if now_card:
            return now_card, 201
        else:
            raise ValidationError(status_code=404, error_code="CVE1001", error_message="card doesn't exist")

    @marshal_with(card_out_fields)
    def post(self):
        args=create_card_parser.parse_args()
        card_title=args.get("card_title", None)
        card_content=args.get("card_content", None)
        card_create_date=datetime.today()
        temp_card_deadline=args.get("card_deadline", None)
        temp2_card_deadline = datetime.strptime(temp_card_deadline, '%Y-%m-%d')
        card_deadline=temp2_card_deadline
        print(card_deadline)
        card_done=args.get("card_done", None)
        if card_done=="on":
            today = datetime.today()
            card_done_date=today
        else:
            card_done_date=None
        card_list_id=args.get("card_list_id", None)

        if card_title is None:
            raise ValidationError(status_code=400, error_code="CVE1002", error_message="card title is required")
        if card_deadline is None:
            raise ValidationError(status_code=400, error_code="CVE1003", error_message="card deadline is required")
        if card_list_id is None:
            raise ValidationError(status_code=400, error_code="CVE1004", error_message="card list_id is required")
            
        new_card=Card(card_title=card_title, card_content=card_content, card_create_date=card_create_date, card_deadline=card_deadline, card_done=card_done, card_done_date=card_done_date, card_list_id=card_list_id)
        db.session.add(new_card)
        db.session.commit()

        return new_card, 201

    @marshal_with(card_out_fields)
    def put(self, card_id):
        args=update_card_parser.parse_args()
        card_title=args.get("card_title", None)
        card_content=args.get("card_content", None)
        temp_card_deadline=args.get("card_deadline", None)
        temp2_card_deadline = datetime.strptime(temp_card_deadline, '%Y-%m-%d')
        print(temp2_card_deadline)
        card_deadline=temp2_card_deadline
        print(card_deadline)
        card_done=args.get("card_done", None)
        if card_done=="on":
            today = datetime.today()
            card_done_date=today
        else:
            card_done_date=None
        print(type(card_deadline))
        card_list_id=args.get("card_list_id", None)

        if card_title is None:
            raise ValidationError(status_code=400, error_code="CVE1002", error_message="card title is required")
        if card_deadline is None:
            raise ValidationError(status_code=400, error_code="CVE1003", error_message="card deadline is required")
        if card_list_id is None:
            raise ValidationError(status_code=400, error_code="CVE1004", error_message="card list_id is required")

        '''now_card_title=Card.query.filter_by(card_title=card_title).first()
        if now_card_title:
            raise ValidationError(status_code=400, error_code="CVE1005", error_message="duplicate card title")
        now_card_content=Card.query.filter_by(card_content=card_content).first()
        if now_card_content:
            raise ValidationError(status_code=400, error_code="CVE1006", error_message="duplicate card content")'''

        new_card=Card.query.filter_by(card_id=card_id).first()
        new_card.card_title=card_title
        new_card.card_content=card_content
        new_card.card_deadline=card_deadline
        new_card.card_done=card_done
        new_card.card_done_date=card_done_date
        new_card.card_list_id=card_list_id
        db.session.commit()

        return new_card, 201

    def delete(self, card_id):
        now_card=Card.query.filter_by(card_id=card_id).first()
        if now_card is None:
            raise ValidationError(status_code=404, error_code="CVE1001", error_message="card doesn't exist")
        db.session.delete(now_card)
        db.session.commit()
        return "", 200

class SummaryAPI(Resource):
    @marshal_with(sum_out_fields)
    def get(self, sum_id):
        now_sum=Summary.query.filter_by(sum_id=sum_id).first()
        if now_sum:
            return now_sum, 201
        else:
            raise ValidationError(status_code=404, error_code="SVE1001", error_message="summary doesn't exist")