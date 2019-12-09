from flask import Flask, render_template, request
import model

app = Flask(__name__)


@app.route('/')
def index():
    return '''
        <img src="/static/drinks.jpg"/>
        <h1>New York City Bar Explorations</h1>
        <ul>
            <li><a href="/neighborhoods">Start from a list of New York Neighborhoods.</a></li>
            <li><a href="/bars'>Dive right into bars.</a></li>
        </ul>
    '''


@app.route('/bars', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
    else:
        firstname = ''
        lastname = ''

    return render_template("hello.html", firstname=firstname, lastname=lastname)


@app.route('/neighborhoods', methods=['GET', 'POST'])
def bball():
    if request.method == 'POST':
        sortby = request.form['sortby']
        sortorder = request.form['sortorder']
        seasons = model.get_bball_seasons(sortby, sortorder)
    else:
        seasons = model.get_bball_seasons()

    return render_template("seasons.html", seasons=seasons)


if __name__ == '__main__':
    model.init_bball()
    app.run(debug=True)
