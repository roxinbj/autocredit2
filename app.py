from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/healthy',methods=['GET'])
def is_healthy():
    return "I am healthy",200


@app.route('/send_sms', methods=['POST'])
def send_sms():
    # Extract phone number and message from the request
    phone_number = request.json.get('phone_number')
    message = request.json.get('message')

    if not phone_number or not message:
        return jsonify({'error': 'Phone number and message are required'}), 400

    # Use gammu to send the SMS
    result = os.system(f'echo "{message}" | sudo gammu sendsms TEXT {phone_number}')
    
    if result == 0:
        return jsonify({'status': 'SMS sent successfully'})
    else:
        return jsonify({'error': 'Failed to send SMS'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
