from flask import Flask, request, redirect
import os
import jinja2

#Use templates (one for the index/home page and one for the welcome page) to render the HTML for your web app.
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    template = jinja_env.get_template('index.html')
    return template.render()


@app.route("/", methods=["POST"])
def validate_user_info():
    username = request.form["username"]
    password = request.form["password"]
    passwordconfirm = request.form["passwordconfirm"]
    email = request.form["email"]

    username_error = ''
    password_error = ''
    passwordconfirm_error = ''
    email_error = ''

#Username errors
#The user leaves any of the following fields empty: username, password, verify password.
#The user's username or password is not valid -- for example, it contains a space character or it consists of less than 3 characters or more than 20 characters (e.g., a username or password of "me" would be invalid).
    if username == '':
        username_error = "You must choose a username."
    elif " " in username:
        username_error = "Your username cannot contain spaces."
    elif len(username) < 3:
        username_error = "Your username is too short."
    elif len(username) > 20:
        username_error = "Your username is too long."


#Initial password errors
#The user leaves any of the following fields empty: username, password, verify password.
#The user's username or password is not valid -- for example, it contains a space character or it consists of less than 3 characters or more than 20 characters (e.g., a username or password of "me" would be invalid).
    if password == '':
        password_error = "You must choose a password."
    elif " " in password:
        password_error = "Your password cannot contain spaces."
    elif len(password) < 3:
        password_error = "Your password is too short."
    elif len(password) > 20:
        password_error = "Your password is too long."


#Confirmation password errors
#The user leaves any of the following fields empty: username, password, verify password.
#The user's password and password-confirmation do not match.
    if passwordconfirm == '':
        passwordconfirm_error = "You must confirm your password."
    elif passwordconfirm != password:
        passwordconfirm_error = "You password entries did not match."


#The user provides an email, but it's not a valid email. Note: the email field may be left empty, but if there is content in it, then it must be validated. The criteria for a valid email address in this assignment are that it has a single @, a single ., contains no spaces, and is between 3 and 20 characters 
    if email == '':
        #only specifying now to avoid issues later; this does not actually DO anything.
        email_error = ''
    elif "@" not in email:
        email_error = "This address does not have an @ symbol."
    elif "." not in email:
        email_error = "This address does not have a . symbol."
    elif " " in email:
        email_error = "Email addresses cannot contain spaces."
    elif len(email) < 3:
        email_error = "This address is too short to be a valid email address."
    elif len(email) > 20:
        email_error = "This address is too long for our form."


#For the username and email fields, you should preserve what the user typed, so they don't have to retype it. With the password fields, you should clear them, for security reasons.
    if not username_error and not password_error and not passwordconfirm_error and not email_error:
        return redirect("/welcome?username={0}".format(username))
    else:
        template = jinja_env.get_template('index.html')
        return template.render(username = username, email = email, username_error = username_error, password_error = password_error, passwordconfirm_error = passwordconfirm_error, email_error = email_error)



#If all the input is valid, then you should redirect the user to a welcome page that uses the username input to display a welcome message of: "Welcome, [username]!"

@app.route('/welcome')
def welcome():
    username = request.args.get("username")
    template = jinja_env.get_template('welcome.html')
    return template.render(name = username)

app.run()