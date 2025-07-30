from flask import Flask, jsonify, request, render_template
from pos_blockchain import PoSBlockchain

app = Flask(__name__)
chain = PoSBlockchain()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/stake', methods=['POST'])
def stake():
    values = request.get_json()
    node = values['node_id']
    amount = values['amount']
    chain.register_node(node, amount)
    return jsonify({'message': f'{node} staked {amount} tokens.'}), 201

@app.route('/mine', methods=['GET'])
def mine():
    block = chain.propose_block()
    response = {
        'message': f"Block {block['index']} created by {block['validator']}.",
        'block': block
    }
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': chain.chain,
        'length': len(chain.chain)
    }
    return jsonify(response), 200

@app.route('/clear', methods=['POST'])
def clear_chain():
    global chain
    # Reset the blockchain while maintaining the same instance
    chain.chain = []
    chain.stakes = {}
    chain.create_block(validator="genesis", previous_hash='0')
    return jsonify({
        'message': 'Blockchain cleared to genesis block',
        'new_chain_length': len(chain.chain)
    }), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)