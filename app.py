from flask import Flask, render_template, request
import model

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/bars', methods=['GET', 'POST'])
def bars():
    if request.method == 'POST':
        nid = request.form['nid']
        fbars = model.get_filtered_bars(nid)
    else:
        nid = ''
        fbars = model.get_filtered_bars()

    return render_template("bars.html", nid=nid, filtered_bars=fbars)


@app.route('/neighborhoods', methods=['GET', 'POST'])
def neighborhoods():
    if request.method == 'POST':
        sortby = request.form['sortby']
        sortorder = request.form['sortorder']
        # neigh_id = request.form['nid']
        nbs = model.get_neighbors(sortby, sortorder)
    else:
        nbs = model.get_neighbors()

    return render_template("neighborhoods.html", nbs=nbs)  # nid= neigh_id


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
    app.run(debug=True)
