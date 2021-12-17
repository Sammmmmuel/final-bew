from flask import Blueprint, request, render_template, redirect, url_for, flash, Flask
from app.main.forms import CompetitionsForm
from app.models import Competitions
from app.models import Event, Competitions, User
from app.main.forms import EventForm, CompetitionsForm
from flask_login import login_required, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt


from app import app, db

main = Blueprint('main', __name__)

bcrypt = Bcrypt(app)

@main.route('/')
def homepage():
    all_events = Event.query.all()
    print(all_events)
    return render_template('home.html', all_events=all_events)

@main.route('/new_event', methods=['GET', 'POST'])
@login_required 
def new_event():
    form=EventForm()

    if form.validate_on_submit():
        new_event= Event(
            title = form.title.data,
            description = form.description.data,
            address = form.address.data
        )
        db.session.add(new_event)
        db.session.commit()

        flash('You have Succesfully created a new competitions event')
        return redirect(url_for('main.event_detail', event_id=new_event.id))
    return render_template('new_event.html', form=form)

@main.route('/event/<event_id>', methods=['GET', 'POST'])
@login_required 
def event_detail(event_id):
    event = Event.query.get(event_id)
    form = EventForm(obj=event)
    
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.address = form.address.data

        db.session.commit()

        flash('You have Succesfully updated your event')
        return redirect(url_for('main.event_detail', event_id=event.id, event=event))
    return render_template('event_detail.html', event=event, form=form)

@main.route('/new_competitions', methods=['GET', 'POST'])
@login_required 
def new_competitions():
    form=CompetitionsForm()

    if form.validate_on_submit():
        new_competitions= Competitions(
            name = form.name.data,
            make_name = form.make_name.data,
            photo_url = form.photo_url.data,
            events = form.events.data
        )
        db.session.add(new_competitions)
        db.session.commit()

        flash('You have successfully added a new competitions to an event')
        return redirect(url_for('main.competitions_detail', competitions_id=new_competitions.id))
    return render_template('new_competitions.html', form=form)

@main.route('/competitions/<competitions_id>', methods=['GET', 'POST'])
@login_required 
def competitions_detail(competitions_id):
    competitions = Competitions.query.get(competitions_id)
    form = CompetitionsForm(obj=competitions)
    
    if form.validate_on_submit():
        competitions.name = form.name.data
        competitions.make_name = form.make_name.data
        competitions.photo_url = form.photo_url.data

        db.session.commit()

        flash('You have Succesfully updated your competitions')
        return redirect(url_for('main.competitions_detail', competitions_id=competitions.id, competitions=competitions))
    return render_template('competitions_detail.html', competitions=competitions, form=form)

@main.route('/competitions_show/<event_id>', methods=['GET', 'POST'])
def competitions_show(event_id):
    event = Event.query.get(event_id)

    return render_template('competitions_show.html', event=event)