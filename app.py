from flask import Flask, request, jsonify
from flask_cors import CORS
import codon_opt

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Web App with Python Flask!'

@app.route('/opt', methods=['POST'])
def opt():
    data = request.get_json()  # dictionary
    species = data['species']
    seq = data['seq']
    output = codon_opt.opt(species, seq)
    if type(output) == str: # encountered an error
        return jsonify({'error':output})
    else:
        return jsonify({'changes':output['changes'],
                        'final':output['final'],
                        'final_seq':output['final_seq']})
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
