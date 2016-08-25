import webapp2
import cgi
import re

UN_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PWD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
    return UN_RE.match(username)

def valid_password(password):
    return PWD_RE.match(password)

def valid_email(email):
    return not email or EMAIL_RE.match(email)

form="""
<form method="post">
<h1>Signup</h1>
<br>
<table>
    <tr>
        <td>Username:</td>
        <td><input type="text" name="username" value="%(username)s"></td>
        <td><span style="color: red">%(unameError)s</span></td>
    </tr>
    <tr>
        <td>Password:</td>
        <td><input type="password" name="password" value="%(password)s"></td>
        <td><span style="color: red">%(pwdError)s</span></td>
    </tr>
    <tr>
        <td>Verify password:</td>
        <td><input type="password" name="verifyPassword" value="%(verifyPassword)s"></td>
        <td><span style="color: red">%(pwdVerError)s</span></td>
    </tr>
    <tr>
        <td>Email (optional):</td>
        <td><input type="text" name="email" value="%(email)s"></td>
        <td><span style="color: red">%(emailError)s</span></td>
    </tr>
</table>

<br>
<input type="submit">
</form>
"""
class MainHandler(webapp2.RequestHandler):
    def write_form(self, username="", unameError="", password="", pwdError="", verifyPassword="",pwdVerError="", email="", emailError=""):
        self.response.out.write(form % {"username": cgi.escape(username),
                                        "unameError": unameError,
                                        "password": cgi.escape(password),
                                        "pwdError": pwdError,
                                        "verifyPassword": cgi.escape(verifyPassword),
                                        "pwdVerError": pwdVerError,
                                        "email": cgi.escape(email),
                                        "emailError": emailError})

    def get(self):
        self.write_form()

    def post(self):
        user_username = self.request.get('username')
        user_password = self.request.get('password')
        user_verifyPassword = self.request.get('verifyPassword')
        user_email = self.request.get('email')
        unameError=""
        pwdError=""
        pwdVerError=""
        emailError =""

        username = valid_username(user_username)
        password = valid_password(user_password)
        verPassword = valid_password(user_verifyPassword)
        email = valid_email(user_email)

        if not username:
            unameError="invalid username"
        if not password:
            pwdError="invalid password"
            user_password = ""
            user_verifyPassword =""
        if not verPassword:
            pwdVerError="invalid password"
            user_password = ""
            user_verifyPassword =""
        if user_password != user_verifyPassword:
            pwdVerError="passwords do not match"
            user_password = ""
            user_verifyPassword =""
        if not email:
            emailError="invalid email"

        if (unameError or pwdError or pwdVerError or emailError):
            self.write_form(user_username,
                        unameError,
                        user_password,
                        pwdError,
                        user_verifyPassword,
                        pwdVerError,
                        user_email,
                        emailError)
        else:
            self.redirect("/welcome?username="+user_username)


class SignupHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        username = cgi.escape(username)
        if valid_username(username):
            self.response.out.write("Welcome "+username+"!")
        else:
            self.redirect("/")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', SignupHandler)
], debug=True)
