from flask import Flask , render_template , request , redirect , url_for , flash , jsonify

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/signup')
def signup():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('login.html')

if __name__ == '__main__':
	app.run(debug=True)