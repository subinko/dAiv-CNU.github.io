from flask import Flask, send_from_directory


app = Flask(__name__, static_url_path="", static_folder="dist/res/static", template_folder="dist/res/templates")


@app.route("/cdn/<path:path>")
def respond_cdn_res(path):
    return send_from_directory("cdn", path)


@app.route("/dist/<path:path>")
def respond_dist_source(path):
    return send_from_directory("dist", path)


@app.route("/", defaults={'path': "", 'file': "index"})
@app.route("/<file>.html", defaults={'path': ""})
@app.route("/<path:path>/", defaults={'file': "index"})
@app.route("/judge/", defaults={'path': "judge", 'file': "index"})  # 없으면 안들어가짐...
@app.route("/<path:path>/<file>.html")
def redirect_to_index(path, file):
    return app.send_static_file(f"{path}/{file}.html" if path else f"{file}.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)

    #hello!