# Integrantes: Diego Henríquez y Diego Morales
# Asignatura: Ciberseguridad en Desarrollo
# Sección: OCY1102


from flask import Flask, request, render_template_string, session, redirect, url_for
import sqlite3
import os
import hashlib
from prometheus_flask_exporter import PrometheusMetrics



app = Flask(__name__)

# --- CONFIGURACIÓN DE SEGURIDAD ---
# Implementado por: Diego Morales

@app.after_request
def add_security_headers(response):
    # 1. Elimina 'Content Security Policy (CSP) Header Not Set'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; "
        "style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com; "
        "font-src 'self' https://maxcdn.bootstrapcdn.com; "
        "img-src 'self' data:;"
    )
    # 2. Elimina 'Missing Anti-clickjacking Header'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    # 3. Elimina 'X-Content-Type-Options Header Missing'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # 4. Elimina 'Permissions Policy Header Not Set'
    response.headers['Permissions-Policy'] = "geolocation=(), microphone=(), camera=()"
    # 5. Elimina 'Server Leaks Version Information...'
    response.headers['Server'] = 'SecurityProxy'
    # 6. Elimina 'Strict-Transport-Security Header Not Set' (HSTS)
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# Configuración de Cookies Seguras
# Implementado por: Diego Morales
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)
# ------------------------------------------------

# Integración de Monitoreo (Prometheus)
# Implementado por: Diego Henríquez
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.3')

app.secret_key = os.urandom(24)

def get_db_connection():
    conn = sqlite3.connect('example.db')
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    return render_template_string('''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet">
            <title>Welcome</title>
        </head>
        <body>
            <div class="container">
                <h1 class="mt-5">Welcome to the Example Application!</h1>
                <p class="lead">This is the home page. Please <a href="/login">login</a>.</p>
            </div>
        </body>
        </html>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()

        # --- CORRECCIÓN DE VULNERABILIDAD CRÍTICA (SQL INJECTION) ---
        # Realizado por: Diego Henríquez
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        hashed_password = hash_password(password)
        user = conn.execute(query, (username, hashed_password)).fetchone()
        # ------------------------------------------------------------

        if user:
            session['user_id'] = user['id']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            return render_template_string('''
                <!doctype html>
                <html lang="en">
                <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet">
                    <title>Login</title>
                </head>
                <body>
                    <div class="container">
                        <h1 class="mt-5">Login</h1>
                        <div class="alert alert-danger" role="alert">Invalid credentials!</div>
                        <form method="post">
                            <div class="form-group">
                                <label for="username">Username</label>
                                <input type="text" class="form-control" id="username" name="username">
                            </div>
                            <div class="form-group">
                                <label for="password">Password</label>
                                <input type="password" class="form-control" id="password" name="password">
                            </div>
                            <button type="submit" class="btn btn-primary">Login</button>
                        </form>
                    </div>
                </body>
                </html>
            ''')
    return render_template_string('''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet">
            <title>Login</title>
        </head>
        <body>
            <div class="container">
                <h1 class="mt-5">Login</h1>
                <form method="post">
                    <div class="form-group">
                        <label for="username">Username</label>
                        <input type="text" class="form-control" id="username" name="username">
                    </div>
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" class="form-control" id="password" name="password">
                    </div>
                    <button type="submit" class="btn btn-primary">Login</button>
                </form>
            </div>
        </body>
        </html>
    ''')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    comments = conn.execute(
        "SELECT comment FROM comments WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()

    return render_template_string('''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet">
            <title>Dashboard</title>
        </head>
        <body>
            <div class="container">
                <h1 class="mt-5">Welcome, user {{ user_id }}!</h1>
                <form action="/submit_comment" method="post">
                    <div class="form-group">
                        <label for="comment">Comment</label>
                        <textarea class="form-control" id="comment" name="comment" rows="3"></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Submit Comment</button>
                </form>
                <h2 class="mt-5">Your Comments</h2>
                <ul class="list-group">
                    {% for comment in comments %}
                        <li class="list-group-item">{{ comment['comment'] }}</li>
                    {% endfor %}
                </ul>
            </div>
        </body>
        </html>
    ''', user_id=user_id, comments=comments)

@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    comment = request.form['comment']
    user_id = session['user_id']

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO comments (user_id, comment) VALUES (?, ?)", (user_id, comment))
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))

@app.route('/admin')
def admin():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    return render_template_string('''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet">
            <title>Admin Panel</title>
        </head>
        <body>
            <div class="container">
                <h1 class="mt-5">Welcome to the admin panel!</h1>
            </div>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)