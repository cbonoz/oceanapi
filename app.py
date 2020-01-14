from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import json
import os
import time
from examples.example_metadata import metadata
from ocean_utils.ddo.metadata import Metadata
from ocean_keeper.account import Account

from squid_py import (
    Ocean,
    ConfigProvider,
    Config,
)

app = Flask(__name__)
CORS(app)

ocean = Ocean(Config('config_local.ini'))
config = ocean.config
account = ocean.accounts.list()#[0] # Take the first account as source.
account = Account(config.parity_address, config.parity_password)

# describe the data available in an existing dataset
@app.route('/describe', methods=['GET'])
def describe():
    asset_id = request.args.get('asset_id')
    path = os.path.join(ocean.config.downloads_path, f'datafile.{asset_id}.0')
    df = pd.read_csv(path, index_col=0, nrows=1)
    # columns = list().columns.tolist())
    columns = df.dtypes.to_dict()
    return jsonify({'columns': columns})

# query an existing dataset
@app.route('/search', methods=['POST'])
def search():
    query = request.args.get('query')
    asset_ddos = ocean.assets.search(query) # ex query: 'Ocean Protocol'
    return jsonify({'data': asset_ddos})

@app.route('/q', methods=['POST'])
def query():
    data = request.json
    query = data.get('query')
    asset_id = data.get('asset_id', None)
    if not asset_id:
        raise Exception('asset_id required')
    path = os.path.join(ocean.config.downloads_path, f'datafile.{asset_id}.0')
    csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
    target = csv_files[0]
    df = pd.read_csv(target, index_col=0, header=0)
    print(asset_id, target, df.info())
    print('query', query)
    rows = df.filter(like=query, axis=0).to_dict('records')
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
