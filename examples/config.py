demo_config = {'keeper-contracts':{
                    # Point to an Ethereum RPC client. Note that Squid learns the name of the network to work with from this client.
                    'keeper.url':'http://localhost:8545',
                    # Specify the keeper contracts artifacts folder (has the smart contracts definitions json files). When you
                    # install the package, the artifacts are automatically picked up from the `keeper-contracts` Python
                    # dependency unless you are using a local ethereum network.
                    'keeper.path':'~/.ocean/keeper-contracts/artifacts',
                    'secret_store.url': 'http://localhost:12001',
                    'parity.url': 'http://localhost:8545',
                    'parity.address': '0x00bd138abd70e2f00903268f3db08f2d25677c9e',
                    'parity.password': 'node0',
                    'parity.address1': '0x068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0',
                    'parity.password1': 'secret',
                },
                'resources': {
                    # aquarius is the metadata store. It stores the assets DDO/DID-document
                    'aquarius.url': 'http://172.15.0.15:5000',
                    # Brizo is the publisher's agent. It serves purchase and requests for both data access and compute services
                    'brizo.url': 'http://localhost:8030',
                    # points to the local database file used for storing temporary information (for instance, pending service agreements).
                    'storage.path': 'squid_py.db',
                    # Where to store downloaded asset files
                    'downloads.path': 'consume-downloads'
                }}
