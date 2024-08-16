from flask import Flask, render_template, request, jsonify
from scripts.searcher import Searcher
from scripts.parser import UrlParser

app = Flask(__name__)

# UrlParser().start()
sc = Searcher()
sc.init_searcher('./data/output/raw.txt')


@app.route('/')
def index(): # put application's code here
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    print(query)
    if not query:
        return 'Not Found Word'

    results = sc.search(query.lower())
    return render_template('index.html', size=len(results), results=results)



if __name__ == '__main__':
    app.run()
