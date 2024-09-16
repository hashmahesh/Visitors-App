from flask import Flask, render_template, url_for, flash, redirect,request,Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visitordata.db'
db = SQLAlchemy(app)


@app.route("/about")
def aboutpage():
    return render_template("about.html")

@app.route("/",methods=['GET', 'POST'])
def home():
    from forms import IntroForm
    form = IntroForm()
    if request.method == 'POST':
        if form.entry.data:
            form.set_value('entry')
            return redirect(url_for('submit'))
        elif form.exit.data:
            form.set_value('exit')
            return redirect(url_for('exit'))
    return render_template('intro.html', form=form)


@app.route("/submit", methods=['GET', 'POST'])
def submit():
    from forms import visitorform
    from data import visitors,card,update_cards,get_unused_cards,card_numbers,put_cards
    form = visitorform()
    # put_cards(card_numbers)
    if form.validate_on_submit() == True and form.Card_no.data is not None:
        if form.purpose.data == 'Other':
            purpose = form.other_purpose.data
        else:
            purpose = form.purpose.data
        new_visitor = visitors(name=form.name.data, purpose=purpose, Card_no = form.Card_no.data)
        db.session.add(new_visitor)
        db.session.commit()
        update_cards(form)
        form.Card_no.choices = get_unused_cards()
        print('Visitor details submitted successfully!')
        return redirect(url_for("home"))
    print("Fusion")
    form.Card_no.choices = get_unused_cards()
    return render_template("submit.html", title="Visitor", form=form)


@app.route("/exit",methods=['GET','POST'])
def exit(): 
    from forms import exitform
    from data import card,visitors,get_used_cards,change_status
    print("Check 1")
    form = exitform()
    if form.validate_on_submit() == True and form.Card_no.data is not None:
        change_status(form) 
        form.Card_no.choices = get_used_cards()
        print(form.errors)
        return redirect(url_for('feedbackpage'))
    form.Card_no.choices = get_used_cards()
    return render_template("exit.html", title = 'Exit Page',form = form)

@app.route("/visitors")
def display_visitors():
    from data import display_details
    all_visitors, existing_cards = display_details()
    # cards_in_use = display_card()
    # db.session.commit()
    # print(cards_in_use)
    return render_template("visitors.html", title="Visitor Records", visitors=all_visitors, cards = existing_cards )


@app.route("/feedback", methods = ['GET','POST'])
def feedbackpage():
    from data import Feedback
    from forms import Feedbackform
    form = Feedbackform()
    print(form.validate_on_submit())
    print(form.errors)
    if form.validate_on_submit():
        service_rating = request.form['service_rating']
        quality_rating = request.form['quality_rating']
        support_rating = request.form['support_rating']
        feedback = Feedback(category1=service_rating, category2=quality_rating, category3=support_rating)
        print(service_rating,quality_rating,support_rating)
        db.session.add(feedback)
        db.session.commit()
        print("feedback submittted !")
        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('home'))
    print("Feedback not submitted ")
    return render_template("feedback.html",form = form)



if __name__ == "__main__":
    app.run(debug=True)
