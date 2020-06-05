from flask import Flask, render_template, request, session
import requests, json, time
from pycdiscount import PyCdiscount

app = Flask(__name__)
app.config["SECRET_KEY"] = "m6PX0zS593J5djmxQfq-dg"


@app.route('/', methods=['GET', 'POST'])
def index():
    response_api = datasApi().json()

    if request.method == 'POST':

        if session.get('historique') is None:
            session['historique'] = {'result': None, 'nbrOfTry': 0}
            session['ListOfTry'] = {1: None}

        a = session.get('historique')
        game(response_api, a)

    else:
        session['historique'] = {'result': None, 'nbrOfTry': 0}
        session['ListOfTry'] = {1: None}
        a = session.get('historique')
    price = float(response_api['Products'][0]['BestOffer']['SalePrice'])
    return render_template('index.html', response=response_api, result=a, price=price)


def datasApi():
    url = "https://api.cdiscount.com/OpenApi/json/Search"
    params = {
        "ApiKey": "0e952750-da42-4014-abc5-4ddee032b8a5",
        "SearchRequest": {
            "Keyword": "tv",
            "SortBy": "",
            "Pagination": {
                "ItemsPerPage": 1,
                "PageNumber": 0
            },
            "Filters": {
                "Price": {
                    "Min": 0,
                    "Max": 0
                },
                "Navigation": "computers",
                "IncludeMarketPlace": 'false',
                "Condition": 'null'
            }
        }
    }
    return requests.post(url, data=json.dumps(params))


response_api = datasApi().json()
print(float(response_api['Products'][0]['BestOffer']['SalePrice']))


def game(response_api, a):
    nbr = int(a['nbrOfTry']) + 1
    a['nbrOfTry'] = nbr

    if float(response_api['Products'][0]['BestOffer']['SalePrice']) == float(request.form['answer']):
        a['result'] = True

    else:
        a['result'] = False

        if float(request.form['answer']) < float(response_api['Products'][0]['BestOffer']['SalePrice']):

            session['ListOfTry'][str(nbr)] = 1

        elif float(request.form['answer']) > float(response_api['Products'][0]['BestOffer']['SalePrice']):

            session['ListOfTry'][str(nbr)] = 0

    session['historique'] = a


if __name__ == '__main__':
    app.run()
