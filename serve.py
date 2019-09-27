from flask import Flask, request, jsonify
import spacy
from spacy.util import minibatch, compounding
import csv
from fuzzywuzzy import fuzz

reader = csv.DictReader(open('assets/stock-table.csv', 'r'))
dict_list = []
for line in reader:
    dict_list.append(line)

nlp2 = spacy.load('tags')

def find_company (company_name):
    tickers = []
    for company in dict_list:
        # print(company['Name'])
        if company['Name'].lower() == company_name.lower():
            tickers.append(company)
        if company_name.lower() in company['Name'].lower():
            tickers.append(company)
    return tickers

find_company('AbbVie Inc.')
app = Flask(__name__)

@app.route("/analyze", methods=['POST'])
def home():
    entities = []
    req_data = request.get_json()
    doc2 = nlp2(req_data['text'])

    for ent in doc2.ents:
        entities.append({'label': ent.label_, 'text': ent.text})
        if ent.label_ == 'company_name':
            companies = find_company(ent.text)
            # print(companies)
            for company in companies:
                entities.append({'label': 'ticker', 'text': company['Ticker']})
        # print(ent.label_, ent.text)
    return jsonify(entities)
    
if __name__ == "__main__":
    app.run(debug=True)