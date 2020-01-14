from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

import pandas as pd
import json
import os
import time
import difflib
from examples.example_metadata import metadata
from examples.config import demo_config
from ocean_utils.ddo.metadata import Metadata
from ocean_keeper.account import Account

from squid_py import (
    Ocean,
    ConfigProvider,
    Config,
)

def json_abort(status_code, data=None):
    if data is None:
        data = {}
    response = jsonify(data)
    response.status_code = status_code
    abort(response)

# Asset files are saved in a folder named after the asset id
def find_csv(asset_id):
    path = os.path.join(ocean.config.downloads_path, f'datafile.{asset_id}.0')
    csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
    return os.path.join(path, csv_files[0]) if csv_files else None

app = Flask(__name__)
CORS(app)
ConfigProvider.set_config(demo_config)

# ocean = Ocean() 
ocean = Ocean(Config('config_local.ini')) # use local or regular config for production pacific network usage.
config = ocean.config
accounts = ocean.accounts.list()
if accounts:
    account = accounts[0] # take first account as primary source.

@app.route('/', methods=['GET'])
def hello():
    return "Welcome to Oceanapi"


# describe the data available in an existing dataset
@app.route('/describe', methods=['GET'])
def describe():
    asset_id = request.args.get('asset_id')
    if not asset_id:
        json_abort(400, {'error': 'asset_id query param required'})
    path = find_csv(asset_id)
    if not path:
        json_abort(400, {'error': 'no csv found'})
    print(path)
    df = pd.read_csv(path, index_col=0, nrows=1)
    columns = list(df.columns.values)
    return jsonify({'columns': columns})

# query existing datasets # TODO: consult live ocean network - using prewarmed datasets for demo.
@app.route('/search', methods=['POST'])
def search():
    query = request.args.get('query')
    # asset_ddos = ocean.assets.search(query) # ex query: 'Ocean Protocol'
    asset_ddos = os.listdir(ocean.config.downloads_path)
    matches = difflib.get_close_matches(query, asset_ddos)
    dids = list(map(lambda x: x.split('.')[1], matches)) # Take the DID
    return jsonify({'data': dids})

@app.route('/q', methods=['POST'])
def query():
    data = request.json
    query = data.get('query')
    asset_id = data.get('asset_id', None)
    if not asset_id:
        json_abort(400, {'error': 'asset_id body param required'})
    path = find_csv(asset_id)
    if not path:
        json_abort(400, {'error': 'no csv found'})
    df = pd.read_csv(path, index_col=0, header=0)
    print('query', query, asset_id, path, df.info())
    rows = df.query(query).to_dict('records')
    return jsonify({'data': rows})


@app.route('/prepare', methods=['POST'])
def prepare():
    data = request.json
    asset_id = data.get('asset_id', None)
    service_agreement_id = ocean.assets.order(asset_id, 0, account)
    return jsonify({'agreement_id': service_agreement_id})

# Upload a new dataset (api)
@app.route('/register', methods=['POST'])
def register():
    metadata = request.json
    ddo = ocean.assets.create(metadata, account)
    # non-blocking, will need to wait a few moments for the data set to upload before use.
    return jsonify({'ddo': ddo})

if __name__ == '__main__':
    app.run(debug=True)
