import json, requests, simplejson
from pprint import pprint
from datetime import datetime, time

# return a string with the response
def define_response(usertext):
    
    companies = json.load(open('stocks.json'))
    usertext = usertext.lower()

    if (usertext == 'status' or usertext == 's'):
        return status(companies)
    if (usertext == 'status detalhado' or usertext == 'sd'):
        return detailed_status(companies)
    else:
        return random_texts(usertext, companies)

# return the random text
def random_texts(text, companies):

    if (text == 'ajuda'):
        return (find_text('ajuda', 'useful'))
    elif (text == 'oi' or text == 'olá'):
        return (find_text('oi', 'random'))
    elif (text == 'composição'):
        return (get_composicao(companies))
    elif (text == 'sair' or text == 'cancelar' or text == 'parar' or text == 'pare'):
        return (find_text('sair', 'useful'))
    else:
        return (find_text('invalido', 'random'))

def get_composicao(companies):
    text = find_text('composicao', 'random')

    for stock in companies['stocks']:
        text += '\n▪ '
        text += stock['code']
        text += ': '
        text += str(stock['share']) + '%'
    
    return text

def status(companies):
    print('1')
    companies_status, updatedat = get_stocks(companies)
    print('2')
    status, error = get_appreciation(companies_status)
    print('3')
    if (error):
        status = error_message(status, companies)

    if (check_time()):
        message += ' (dados do último dia de funcionamento da bolsa)'

    return 'Valorização: ' + status

def detailed_status(companies):
    companies_status, updatedat = get_stocks(companies)

    status, error = get_appreciation(companies_status)

    if (error):
        status = error_message(status, companies)
    
    message = ''

    for stock in companies['stocks']:
        message += '\n▪ '
        message += stock['code']
        message += ': '
        message += str(stock['status']) + '%'

    message += '\n'

    message += find_text('website', 'useful') + '\n\n'
    message += 'Valorização: ' + status
    
    if (check_time()):
        message += ' (dados do último dia de funcionamento da bolsa)'
    
    return message

def check_time():
    now = datetime.now()
    now_time = now.time()
    if (time(22,01) <= now.time() <= time(12,25)):
        return True
    else:
        return False

# Return error message case one or more stocks has errors and send detailed infos to user
def error_message(status, companies):
    errormessage = find_text('erro', 'useful')

    for stock in companies['stocks']:
        errormessage += '▪ '
        errormessage += stock['code']
        errormessage += ': '
        if (stock['status']['valid'] != 0):
            errormessage += 'ERRO!\n'
        else:
            errormessage += str(stock['status']) + '%\n'
    
    return errormessage

def get_stocks(companies):
    data = json.loads(requests.get('http://alepmaros.me/monetus/stocks/').content)
    updatedat = data['last_day_updated']

    for stock in data['last_stocks_updated']:
        dataCode = stock['fields']['code']
        
        for company in companies['stocks']:
            if (company['code'] == dataCode):
                company['status'] = stock['fields']['vcp']

    return companies, updatedat

# valid: 0 caso seja um retorno válido
# valid: 1 caso algum atributo do objeto
# valid: 2 caso haja uma falha na API
def get_company_status(company):
    rsp = requests.get('https://finance.google.com/finance?q=' + company + '&output=json')

    if (rsp.status_code == 200):
        try:
            company_data = json.loads(rsp.content[6:-2].decode('unicode_escape'))

            response = {
                'valid': 0,
                'cp': float(company_data['cp'])
            }

        except:
            response = {
                'valid': 1
            }
    else:
        response = {
            'valid': 2
        }
    
    return response

# return Monetus appreciation at this moment as a string in format (value)%
def get_appreciation(companies):
    total = 0
    error = False
    for stock in companies['stocks']:
        cp = stock['status']
        share = stock['share']
        total += (share / 100) * cp

    appreciation = str(round(total, 2)) + '%'
    
    return (appreciation, error)

# search in texts.json the corresponding text
def find_text(name, kind):
    texts = json.load(open('texts.json'))

    for x in range(0, len(texts[kind])):
        if (texts[kind][x]['name'] == name):
            return texts[kind][x]['text']


def messaging_events(payload):
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]
    for event in messaging_events:
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
        else:
            yield event["sender"]["id"], "I can't echo this"
