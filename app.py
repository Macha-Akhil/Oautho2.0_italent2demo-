from flask import Flask,render_template, request, redirect, session, jsonify,url_for
import requests

app = Flask(__name__)
app.secret_key = 'ZTspnQDqSPJJ8XLZCaJgwMr5MVTOicvQm3OJ0eUx6oc='

@app.route('/hello')
def hello():
    return "Hello:"

@app.route('/')
def home():
    link = {'name': 'italent2', 'url': 'https://italent2.demo.lithium.com/auth/oauth2/authorize?client_id=4bt84GFIquIqQojRIMwpoz2eu9sqB2Q8DRiVcFKo87g=&response_type=code&redirect_uri=http://127.0.0.1:5001/callback'}
    return render_template('index.html',link=link)

@app.route('/callback',methods=['GET'])
def callback():
    endpoint = 'https://italent2.demo.lithium.com//api/2.0/auth/accessToken'
    headers = {
        'Content-Type': 'application/json',
        'client-id': '4bt84GFIquIqQojRIMwpoz2eu9sqB2Q8DRiVcFKo87g='
    }

    # session is used to store the data and it is not shown in the url 
    # it is python library used to store data in session
    session_code = request.args.get('code')
    #return session_code

    # Data payload
    data = {
        'client_id': '4bt84GFIquIqQojRIMwpoz2eu9sqB2Q8DRiVcFKo87g=',
        'client_secret': 'ZTspnQDqSPJJ8XLZCaJgwMr5MVTOicvQm3OJ0eUx6oc=',
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://127.0.0.1:5001/callback',
        'code': session_code  # Assuming you pass the code in the request body JSON
    }
    #return data
    try:
        # Sending POST request
        response = requests.post(endpoint, headers=headers, json=data)
        response_data = response.json()
        #return jsonify(response_data), response.status_code
        if response.status_code == 200:
            # response_data is in data dict ;;
            access_token = response_data['data'].get('access_token')
            # Store access_token in session
            session['access_token'] = access_token
            # return session.get('access_token')
            return redirect(url_for('messages'))#, token=access_token))
            #return redirect(f"http://localhost:3000?access_token={access_token}")
        else:
            return jsonify(response_data), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/messages', methods=['GET'])
def messages():
    #token = request.args.get('token')
    #return token
    # Retrieve access_token from session
    token = session.get('access_token')
    #return token

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get('https://italent2.demo.lithium.com/api/2.0/search?q=select subject,body from messages', headers=headers)
    messages = response.json().get('data', {}).get('items', [])
    #return messages
    return render_template('messages.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

