
import os
import unittest

from datetime import date
 
from app import app, db, bcrypt
from app.models import Competitions, Event, User



#################################################
# Setup
#################################################

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_events():
    a1 = Event(
        title='Bring the beatles back',
        description='Bringing together old classic beatles',
        address='mission st'
    )
    db.session.add(a1)
    db.session.commit()

def create_user():
    # Creates a user with username 'me1' and password of 'password'
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################

class MainTests(unittest.TestCase):
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
    def test_homepage_logged_out(self):
        """Test that the events show up on the homepage."""
        create_events()
        create_user()

        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Competition Events', response_text)
        self.assertIn('All Events', response_text)
        self.assertIn('Home', response_text)
        self.assertIn('Log In', response_text)
        self.assertIn('Sign Up', response_text)

        self.assertNotIn('New Event', response_text)
        self.assertNotIn('Add Competition to Event', response_text)
        self.assertNotIn('Log Out', response_text)
 
    def test_homepage_logged_in(self):
        """Test that the events show up on the homepage."""
        create_events()
        create_user()
        login(self.app, 'me1', 'password')

        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('COMPETITIONS', response_text)
        self.assertIn('All Events', response_text)
        self.assertIn('Home', response_text)
        self.assertIn('Log In', response_text)
        self.assertIn('Sign Up', response_text)

        self.assertNotIn('Log In', response_text)
        self.assertNotIn('Sign Up', response_text)

