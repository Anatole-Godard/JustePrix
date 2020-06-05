from flask import Flask, render_template, request, session
import requests, json, time, random

app = Flask(__name__)
app.config["SECRET_KEY"] = "m6PX0zS593J5djmxQfq-dg"


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method != 'POST':
        d = {1: 'tv', 2: 'jeux vidéo', 3: 'piscine', 4: 'trampoline', 5: 'enceinte'}
        itemrand = random.choice(list(d.values()))
        session['item'] = itemrand


    response_api = datasApi(session['item']).json()

    if request.method == 'POST':

        if session.get('historique') is None:
            session['historique'] = {'result': None, 'nbrOfTry': 0}
            session['ListOfTry'] = {1: None}

        count = session['historique']['nbrOfTry'] + 1
        lastgameT = session['time'][str(count)]

        session['lastAnswer'][str(count)] = float(request.form['answer'])

        tdif = time.time() - lastgameT
        session['time'][str(count)] = "%.2f" % tdif
        newCount = count + 1
        session['time'][str(newCount)] = time.time()

        a = session.get('historique')
        game(response_api, a)

    else:
        session['historique'] = {'result': None, 'nbrOfTry': 0}
        session['ListOfTry'] = {1: None}
        session['time'] = {1: time.time()}
        session['lastAnswer'] = {1: 0}

        a = session.get('historique')
    price = float(response_api['Products'][0]['BestOffer']['SalePrice'])
    Description = response_api['Products'][0]['Description']

    return render_template('index.html', response=response_api, result=a, price=price, Description=Description)


def datasApi(itemrand):
    url = "https://api.cdiscount.com/OpenApi/json/Search"
    params = {
        "ApiKey": "0e952750-da42-4014-abc5-4ddee032b8a5",
        "SearchRequest": {
            "Keyword": session['item'],
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
                "Navigation": itemrand,
                "IncludeMarketPlace": 'false',
                "Condition": 'null'
            }
        }
    }
    return requests.post(url, data=json.dumps(params))




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
    app.run(host='0.0.0.0')
