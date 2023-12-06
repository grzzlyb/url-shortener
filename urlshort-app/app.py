from flask import Flask, request, render_template, redirect, session
import psycopg2
import random, string
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'qwerty'

db_params = {
    'dbname': 'master',
    'user': 'postgres',
    'password': 'pacc',
    'host': 'localhost',
    'port': '5432'
}

@app.route('/home')
@app.route('/login')
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()

        if user:
            session['username'] = username
            return redirect('/base')
        else:
            return render_template('login.html', message='Invalid credentials')

    return render_template('login.html', message='')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    if 'username' in session:
        original_url = request.form['url']
        expires_at = datetime.now() + timedelta(hours=48)

        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM urls WHERE original_url = %s", (original_url,))
        existing_url = cur.fetchone()

        if existing_url:
            short_url = existing_url[2]
        else:
            short_url = generate_short_url()
            cur.execute("INSERT INTO urls (original_url, short_url, username, expires_at) VALUES (%s, %s, %s, %s)",
                        (original_url, short_url, session['username'], expires_at))
            conn.commit()
        conn.close()
        return render_template('dashboard.html', short_url=short_url)
    else:
        return redirect('/')

@app.route('/<short_url>')
def redirect_to_url(short_url):
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    cur.execute("SELECT original_url, expires_at FROM urls WHERE short_url = %s", (short_url,))
    url_data = cur.fetchone()

    if url_data:
        original_url, expires_at = url_data
        if expires_at and expires_at >= datetime.now():
            cur.execute("UPDATE urls SET clicks = clicks + 1 WHERE short_url = %s", (short_url,))
            conn.commit()
            conn.close()
            return redirect(original_url)
        else:
            conn.close()
            return render_template('404.html'), 404
    else:
        conn.close()
        return render_template('404.html'), 404

def generate_short_url():
    characters = string.ascii_lowercase + string.digits
    url_string = ''.join(random.choice(characters) for _ in range(7))
    return url_string

@app.route('/base', methods=['GET', 'POST'])
def base():
    user_urls = []
    username = session.get('username')

    if 'username' in session:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        cur.execute("SELECT original_url, short_url, clicks FROM urls WHERE username = %s", (session['username'],))
        user_urls = cur.fetchall()

        conn.close()
    else:
        return redirect('/login')

    if request.method == 'POST':
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        original_url = request.form['url']
        expires_at = datetime.now() + timedelta(hours=48)
        cur.execute("SELECT * FROM urls WHERE original_url = %s AND username = %s", (original_url, session['username']))
        existing_url = cur.fetchone()

        if existing_url:
            short_url = existing_url[2]
        else:
            short_url = generate_short_url()
            cur.execute("INSERT INTO urls (original_url, short_url, username, expires_at) VALUES (%s, %s, %s, %s)",
                        (original_url, short_url, session['username'], expires_at))
            conn.commit()
        cur.execute("SELECT original_url, short_url, clicks FROM urls WHERE username = %s", (session['username'],))
        user_urls = cur.fetchall()
        conn.close()
        username = session.get('username')
        return render_template('base.html', short_url=short_url, user_urls=user_urls, username=username)
    else:
        return render_template('base.html', user_urls=user_urls, username=username)

@app.route('/history')
def history():
    if 'username' in session:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute("SELECT short_url, clicks FROM urls WHERE username = %s", (session['username'],))
        user_urls = cur.fetchall()

        conn.close()
        return render_template('history.html', user_urls=user_urls)
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)