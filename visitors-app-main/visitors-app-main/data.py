from app import app,db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta


class visitors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    purpose = db.Column(db.String(50))
    date_visited = db.Column(db.DateTime, nullable=False, default=datetime.utcnow() + timedelta(hours = 5, minutes= 30))
    date_left = db.Column(db.DateTime)
    Card_no = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"visitors('{self.name}','{self.purpose}',{self.Card_no})"

class card(db.Model):
    Card_no = db.Column(db.Integer,primary_key = True)
    status = db.Column(db.Boolean,default = False)
    def __repr__(self):
        return f"visitors({self.Card_no},{self.status})"

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category1 = db.Column(db.Integer, nullable = False)
    category2 = db.Column(db.Integer, nullable = False)
    category3 = db.Column(db.Integer, nullable = False)
    def __repr__(self):
        return f"visitors({self.category1},{self.category2},{self.category3})"

temp = card()
card_numbers =[1,2,3,4,5,6,7,8,9,10]

def put_cards(card_numbers):
  with app.app_context():
    for card_number in card_numbers:
      existing_card = card.query.filter_by(Card_no=card_number).first()
      if not existing_card:
        new_card = card(Card_no=card_number)
        db.session.add(new_card)
      else:
        print(f"Card number {card_number} already exists in the database.")
        db.session.commit()


def update_cards(form):
   with app.app_context():
      new_card = card.query.filter_by(Card_no=form.Card_no.data).first()
      new_card.status = True
      db.session.commit()
      return "Update successful!"

def get_cards():
    with app.app_context():
        cards=card.query.all()
        c_list=[]
        for i in cards:
            c_list.append(i.Card_no)
    print(c_list)
    return c_list

def display_details():
   with app.app_context():
      all_visitors = visitors.query.all()
      return all_visitors, display_card()
   
def display_card():
    with app.app_context():
      cards_in_use = card.query.filter_by(status = True).all()
      return cards_in_use

def get_used_cards():
    with app.app_context():
        cards=card.query.filter_by(status = True)
        c_list=[]
        for i in cards:
            c_list.append(i.Card_no)
    print(c_list)
    return c_list

def get_unused_cards():
   with app.app_context():
        cards=card.query.filter_by(status = False)
        c_list=[]
        for i in cards:
            c_list.append(i.Card_no)
        return c_list

def change_status(form):
   with app.app_context():
        card_in_use = card.query.filter_by(Card_no=form.Card_no.data).first()
        card_in_use.status = False
        db.session.commit()
        card_number = form.Card_no.data
        exit_datetime = datetime.utcnow() + timedelta(hours = 5, minutes= 30)
        visitor = visitors.query.filter_by(Card_no=card_number , date_left = None).first()
        if visitor:
            visitor.date_left = exit_datetime
            db.session.commit()
            print(f"Exit time noted for visitor with Card_no {card_number}")
            return "Exit time noted!"
        else:
            print(f"Visitor with Card_no {card_number} not found.")
            return "Visitor not found!"
        
def test():
   with app.app_context():
      db.create_all()



        
