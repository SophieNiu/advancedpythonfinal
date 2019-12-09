from flask import Flask, render_template, request
import model

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/bars', methods=['GET', 'POST'])
def bars():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
    else:
        firstname = ''
        lastname = ''

    return render_template("bars.html", firstname=firstname, lastname=lastname)


@app.route('/neighborhoods', methods=['GET', 'POST'])
def neighborhoods():
    if request.method == 'POST':
        sortby = request.form['sortby']
        sortorder = request.form['sortorder']
        neigh_id = request.form['nid']
        nbs = model.get_neighbors(sortby, sortorder)
    else:
        neigh_id = ''
        nbs = model.get_neighbors()

    return render_template("neighborhoods.html", nid=neigh_id, neighborhoods=nbs)


@app.route('/bardetail', methods=['GET'])
def bardetail():
    if request.method == 'POST':
        sortby = request.form['sortby']
        sortorder = request.form['sortorder']
        seasons = model.get_neighbors(sortby, sortorder)
    else:
        seasons = model.get_neighbors()

    return render_template("bardetail.html", seasons=seasons)


if __name__ == '__main__':
    model.init_neighbors()
    print('here we go', app.name)
    app.run(debug=True)
