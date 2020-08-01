from flask import Flask, jsonify, request, render_template
import requests
import os

app = Flask(__name__)

app.config['FLASK_RUN_PORT'] = os.environ.get('LISTEN')
# print(app.config)


def get_comic_data(id_for_url):
    # Function to handle requests
    if id_for_url == "current":
        URL = 'http://xkcd.com/info.0.json'
    else:
        URL = f"http://xkcd.com/{id_for_url}/info.0.json"

    r = requests.get(url=URL)
    if r.status_code != 200:
        return jsonify({"ERROR": "Comic ID not found."})

    data = r.json()
    current_data = {
        'id': data['num'],
        'description': data['alt'],  # or transcript?
        'date': f"{data['year']}-{data['month']}-{data['day']}",
        'title': data['title'].lower(),
        'url': data['img']
    }
    return current_data


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/comics/current', methods=['GET'])
def current_comic():
    return jsonify(get_comic_data("current"))


@app.route('/comics/<comic_id>', methods=['GET'])
def specific_comic(comic_id):
    try:
        int(comic_id)
    except ValueError:
        return jsonify({"ERROR": "Comic ID should be an integer."}), 404

    return jsonify(get_comic_data(comic_id))


@app.route('/comics/many/', methods=['GET'])
def many_comics():
    # Get all of the ids:
    ids_list = request.args.getlist("comic_ids")
    # Take only unique values:
    unique_ids = list(dict.fromkeys(ids_list))

    comics = []
    for comic in unique_ids:
        comics.append(get_comic_data(comic))

    return jsonify(comics)


if __name__ == '__main__':
    app.run()
