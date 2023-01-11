import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import sqlite3 as sql
import hashlib

st.set_page_config(page_title="ByBit-AI", page_icon="static/image.png")


def hash_password(password):
		return hashlib.sha256(password.encode()).hexdigest()

class DB():
	def __init__(self, db_name):
		self.db_name = db_name
		self.conn = sql.connect(self.db_name)
		self.cursor = self.conn.cursor()
		self.cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT , mail TEXT , password TEXT)")
		self.conn.commit()

	def add_user(self, username, mail , password):
		password = hash_password(password)
		self.cursor.execute("INSERT INTO users VALUES (?, ? , ?)", (username, mail, password))
		self.conn.commit()

	def check_user(self, username):
		self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
		if self.cursor.fetchone():
			return True
		else:
			return False

	def login(self, username, password):
		password = hash_password(password)
		self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
		if self.cursor.fetchone():
			return True
		else:
			return False
		

class API_KEYS(DB):
	def __init__(self, db_name):
		super().__init__(db_name)
		self.cursor.execute("CREATE TABLE IF NOT EXISTS api_keys (username TEXT, api_key TEXT, api_secret TEXT)")
		self.conn.commit()
	def add_api_key(self, username, api_key, api_secret):
		self.cursor.execute("INSERT INTO api_keys VALUES (?, ?, ?)", (username, api_key, api_secret))
		self.conn.commit()
	def remove_api_key(self, username):
		self.cursor.execute("DELETE FROM api_keys WHERE username = ?", (username,))
		self.conn.commit()
	def get_api_key(self, username):
		self.cursor.execute("SELECT * FROM api_keys WHERE username = ?", (username,))
		return self.cursor.fetchone()
	def check_api_key(self, username, api_key, api_secret):
		self.cursor.execute("SELECT * FROM	api_keys WHERE username = ? AND api_key = ? AND api_secret = ?", (username, api_key, api_secret))
		if self.cursor.fetchone():
			return True
		else:
			return False

if "page" not in st.session_state:
	st.session_state.page = "home"

if "logged" not in st.session_state:
	st.session_state.logged = False


db = DB("db.db")

def nav_bar():
	other , icone , home , sing_up , login , other2 = st.columns(6)
	with icone:
		st.image("icones/logo-no-bg.png" , width=150)
	with home:
		st.markdown("###")
		if st.button("home"):
			st.session_state.page = "home"
			st.experimental_rerun()
	with sing_up:
		st.markdown("###")
		if st.button("Sign up"):
			st.session_state.page = "sign_up"
			st.experimental_rerun()
	with login:
		st.markdown("###")
		if st.button("Login"):
			st.session_state.page = "login"
			st.experimental_rerun()
	

def nav_bar_logged():
	st.sidebar.image("icones/logo-no-bg.png" , width=300)
	if st.sidebar.button("Market"):
		st.session_state.page = "market"
		st.experimental_rerun()
	if st.sidebar.button("Portfolio"):
		st.session_state.page = "portfolio"
		st.experimental_rerun()
	if st.sidebar.button("API Keys"):
		st.session_state.page = "api_keys"
		st.experimental_rerun()
	if st.sidebar.button("Log out"):
		st.session_state.page = "home"
		st.session_state.logged = False
		st.experimental_rerun()


def home():
	nav_bar()
	left , right = st.columns(2)
	st.markdown("___")
	with left:
		st.image("static/image.png" , use_column_width=True)
	with right:
		st.title("ByBit-AI")
		st.write("""
		Introducing ByBit-AI, the revolutionary new platform that uses artificial intelligence to trade assets.
		Our cutting-edge AI algorithms analyze market trends and make trades with lightning-fast speed and accuracy.
		With ByBit-AI, you can sit back and watch your portfolio grow without lifting a finger. Try it out today and see the power of AI at work!""")
	
	c1, c2 , c3 = st.columns(3)
	with c1:
		pass
	with c2:
		st.title("Features")
	with c3:
		pass
	st.markdown("###")

	col1 , col2 , col3 = st.columns(3)
	with col1:
		st.write("<h2>Automated trades:</h2>" , unsafe_allow_html=True)
		st.write("Using AI algorithms, ByBit-AI can automatically place trades on your behalf, based on market trends and other factors.")
	with col2:
		st.write("<h2>User-friendly interface:</h2>" , unsafe_allow_html=True)
		st.write("The ByBit-AI platform is designed with usability in mind, so you can easily monitor and manage your trades.")
	with col3:
		st.write("<h2>Real-time monitoring:</h2>" , unsafe_allow_html=True)
		st.write("ByBit-AI provides real-time updates and alerts on your portfolio, so you can stay informed about what's happening at all times.")
	st.markdown("___")

	left1 , right1 = st.columns(2)
	with left1:
		st.image("icones/graph.png", use_column_width=True)
	with right1:
		st.write("With ByBit-AI, you can take the guesswork out of investing. Our AI algorithms do the heavy lifting for you, analyzing market trends and making trades that are designed to maximize your profits. Whether you're an experienced investor or new to the game, ByBit-AI makes it easy to get started and start seeing returns.")
	st.markdown("___")
	
	left2, right2 = st.columns(2)
	with left2:
		st.write("Don't let a busy schedule hold you back from growing your wealth. With ByBit-AI, you can set up your trades and let the AI do the rest. Whether you're at work, on vacation, or just too busy to keep up with the markets, ByBit-AI has you covered.")
	with right2:
		st.image("icones/busy.png", use_column_width=True)

def sing_up():
	nav_bar()
	st.title("Sign up")
	st.markdown("___")
	username = st.text_input("Username")
	mail = st.text_input("Mail")
	password = st.text_input("Password" , type="password")
	if st.button("Sign up", key="sign_up"):
		if not db.check_user(username):
			db.add_user(username, mail, password)
			st.success("Account created")
			st.session_state.page = "login"
			st.experimental_rerun()
		else:
			st.error("Username already exist")

def login():
	nav_bar()
	st.title("Login")
	st.markdown("___")
	username = st.text_input("Username")
	password = st.text_input("Password" , type="password")
	if st.button("Login", key="login"):
		if db.check_user(username):
			if db.login(username, password):
				st.success("Logged in")
				st.session_state.page = "dashboard"
				st.session_state.logged = True
				st.experimental_rerun()
			else:
				st.error("Wrong password")
		else:
			st.error("User not found")

def dashboard():
	nav_bar_logged()

def market():
	nav_bar_logged()

def api_keys():
	nav_bar_logged()

def portfolio():
	nav_bar_logged()

	
if st.session_state.page == "home":
	home()
if st.session_state.page == "sign_up":
	sing_up()
if st.session_state.page == "login":
	login()
if st.session_state.page == "dashboard" and st.session_state.logged:
	dashboard()
if st.session_state.page == "market" and st.session_state.logged:
	market()
if st.session_state.page == "api_keys" and st.session_state.logged:
	api_keys()
if st.session_state.page == "portfolio" and st.session_state.logged:
	portfolio()
