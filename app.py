import os
from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, redirect, url_for, request, session, g, url_for, abort, render_template, flash
from flask_dance.contrib.github import make_github_blueprint, github
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
github_bp = make_github_blueprint(scope="repo")
app.register_blueprint(github_bp, url_prefix="/login")

@app.route("/github/", methods=['GET', 'POST'])
def connect_github():
    if not github.authorized:
        return redirect(url_for("github.login"))

    resp = github.get("/user")

    error = None
    if not resp.ok:
        error = "Problem connecting github"

    gh_content = {'github':github, 'response': resp}
    return render_template('mainform.html', content=gh_content, error=error) #"You are client: {client} with secert on GitHub, yay!".format(client=github.token['access_token'])
# gh_content = {'github':github, 'response': resp}
# return render_template('mainform.html', content=gh_content, error=error)

@app.route('/let_there_be_rainbows_and_puppies/', methods=['GET', 'POST'])
def mainform():
    if not github.authorized:
        return redirect(url_for("github.login"))

    resp = github.get("/user")
    error = None
    if not resp.ok:
        error = "Problem connecting github"


    class MainForm(FlaskForm):
        org = StringField('Github user/organisation',
                           default=resp.json()['login'],
                           validators=[DataRequired()])
        name = StringField('project name', 
                           validators=[DataRequired()])
        language = StringField('project name', 
                               default='python',
                               validators=[DataRequired()])

    form = MainForm()
    if form.validate_on_submit():
        return redirect('/and_cats_as_well', language=form.language.data,
                        org=form.org.data, username=form.name.data,
                        provider='github')

    gh_content = {'github':github, 'response': resp}

    return render_template('mainform.html', form=form, content=gh_content,
                           error=error)

@app.route('/and_cats_as_well/')
def do_the_doing():
    return "Well done! Judges are 3l33t!"
    # if not github.authorized:
    #     return "What are you doing here, Sir?"
    # from lettherebe.registry import repository_host
    # repository_host.members[request.args.get('provider')](
    #     github.token['access_token'], None, "Puppies are nice"
    # )

@app.route("/", methods=['GET', 'POST'])
def index():
    error=None
    if github.authorized:
        return mainform()
    return render_template('login.html', error=error)

if __name__ == "__main__":
    app.run()
