
import os
from unittest import TestCase

from datetime import date
 
from app import app, db, bcrypt
from app.models import Competitions, Event, User


#################################################
# Setup
#################################################

def create_event():
    a1 = Event(
        title='Bring the beatles back',
        description='Bringing together old classic beatles',
        address='mission st'
    )
    db.session.add(a1)
    db.session.commit()

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################

class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup(self):
        post_data = {
            'username': 'me2',
            'password': 'password'
        }

        self.app.post('/signup', data=post_data)

        user = User.query.filter_by(username='me2').one()
        self.assertIsNotNone(user)

    def test_signup_existing_user(self):
        create_user()
        
        post_data = {
            'username': 'me1',
            'password': 'password'
        }
        response = self.app.post('/signup', data=post_data)
        response_text = response.get_data(as_text=True)

        self.assertIn('That username is taken. Please choose a different one.', response_text)
    def test_login_correct_password(self):
        create_user()

        post_data = {
            'username': 'me1',
            'password': 'password'
        }
        self.app.post('/login', data=post_data)
        
        response = self.app.get('/')
        response_text = response.get_data(as_text=True)

        self.assertNotIn('Log In', response_text)

    def test_login_nonexistent_user(self):
        post_data = {
            'username': 'me3',
            'password': 'password'
        }
        
        response = self.app.post('/login', data=post_data)
    
        response_text = response.get_data(as_text=True)

        self.assertIn('Log In', response_text)
        self.assertIn('No user with that username. Please try again.', response_text)

    def test_login_incorrect_password(self):
        create_user()

        post_data = {
            'username': 'me1',
            'password': 'wrong_password'
        }

        response = self.app.post('/login', data=post_data)
    
        response_text = response.get_data(as_text=True)
        self.assertIn('Log In', response_text)
        self.assertIn('Password doesn&#39;t match. Please try again.', response_text)

    def test_logout(self):
        create_user()

        post_data = {
            'username': 'me1',
            'password': 'password'
        }

        self.app.post('/login', data=post_data)
        self.app.get('/logout')

        response = self.app.get('/')
        response_text = response.get_data(as_text=True)

        self.assertIn('Log In', response_text)