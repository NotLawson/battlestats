## Auth module
## Contains the authentication system for the webserver
import os, sys, json, time, logging
from datetime import datetime
from __main__ import database, app

logger = app.logger

def auth(request):
    """
    Authenticates a user per page. This would be used at the very top of 
    each view to ensure the user is authenticated. This will return a user
    id, from which the app can get the user information.
    This function will only login the user via the session token, not username
    and pasword. For that, please see the login function.

    If valid, will return user id (str).
    If invalid, will return False.
    """
    session_token = request.cookies.get("session_token")
    if session_token is None:
        return False
    # Check if the session token is valid
    try:
        return database.get_session(session_token)[0]
    except TypeError:
        return False 
    
def login(username, password):
    """
    Logs in a user via username and password. This will return a session token
    which can be used to authenticate the user for the rest of the session.
    This function will also create a session in the database for the user.

    If valid, will return session token (str).
    If invalid, will return False.
    """
    # Check if the username and password are valid
    try:
        user = database.get_user_authed(username, password)[0]
        database.execute("UPDATE users SET last_login = %s WHERE username = %s AND password = %s", (datetime.now(), username, str(password)))
        # Create a session for the user
        session_token = database.create_session(user, "Session created via login")
        return session_token
    except TypeError:
        return False
    
def signup(username, password, email, battletabs_token, battletabs_id, battletabs_username, fleets):
    """
    Signs up a user via username, password, email, and battletabs token.
    This will return True if created successfully. This function will also create a user in the 
    database for the user.

    If valid, will return True.
    If invalid, will return False.
    """
    # Check if the username and password are valid
    try:
        database.create_user(username, password, email, battletabs_token, battletabs_id, battletabs_username, fleets, ["standard", "inactive"])
        return True
    except Exception as e:
        logger.error(f"Error signing up user: {e}")
        return False



