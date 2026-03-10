from flask import Flask, jsonify, render_template_string, request, redirect, url_for, flash, session, g
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import secrets
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Request ID middleware
@app.before_request
def before_request():
    g.request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{g.request_id}] {request.method} {request.path}")

@app.after_request
def after_request(response):
    logger.info(f"[{g.request_id}] Status: {response.status_code}")
    response.headers['X-Request-ID'] = g.request_id
    return response

# Health check endpoint
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'request_id': g.request_id}), 200

# Error handlers
@app.errorhandler(404)
def not_found(e):
    logger.warning(f"404 Not Found: {request.path}")
    return jsonify({'error': 'Not Found', 'message': 'Resource not found'}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"500 Internal Error: {e}")
    return jsonify({'error': 'Internal Server Error', 'message': 'Something went wrong'}), 500

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class
class User(UserMixin):
    def __init__(self, id, username, email, password_hash, is_admin=False):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin

@login_manager.user_loader
def load_user(user_id):
    return USERS.get(int(user_id))

# In-memory data storage
USERS = {}
DOMAINS = [
    {"name": "example.free", "status": "available", "price": "Free", "owner_id": None, "created_at": None, "expires_at": None},
    {"name": "mydomain.free", "status": "available", "price": "Free", "owner_id": None, "created_at": None, "expires_at": None},
    {"name": "testsite.free", "status": "taken", "price": "N/A", "owner_id": 1, "created_at": "2024-01-15", "expires_at": "2025-01-15"},
]

DNS_RECORDS = {}
USER_COUNTER = 1

# Base HTML template with navigation
BASE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }} - FreeDomain</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .navbar { background: rgba(0,0,0,0.3); padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
        .navbar .brand { color: white; font-size: 24px; font-weight: bold; text-decoration: none; }
        .navbar .nav-links a { color: white; text-decoration: none; margin-left: 20px; padding: 8px 15px; border-radius: 5px; transition: background 0.3s; }
        .navbar .nav-links a:hover { background: rgba(255,255,255,0.2); }
        .container { max-width: 1000px; margin: 40px auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        .hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px; border-radius: 15px; text-align: center; margin-bottom: 30px; }
        .hero h1 { font-size: 48px; margin-bottom: 10px; }
        .hero p { font-size: 20px; opacity: 0.9; }
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 30px; }
        .feature { padding: 30px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 10px; text-align: center; }
        .feature h3 { color: #2c3e50; margin-bottom: 10px; }
        .btn { display: inline-block; padding: 12px 30px; background: #27ae60; color: white; text-decoration: none; border-radius: 25px; margin: 5px; transition: transform 0.3s, box-shadow 0.3s; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
        .btn-primary { background: #3498db; }
        .btn-danger { background: #e74c3c; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 15px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #3498db; color: white; }
        tr:hover { background: #f5f5f5; }
        .available { color: #27ae60; font-weight: bold; }
        .taken { color: #e74c3c; font-weight: bold; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: bold; color: #2c3e50; }
        .form-group input, .form-group select { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; }
        .form-group input:focus { border-color: #3498db; outline: none; }
        .alert { padding: 15px; border-radius: 8px; margin: 15px 0; }
        .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .alert-error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .alert-info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .stat-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px; text-align: center; }
        .stat-card h2 { font-size: 36px; margin-bottom: 5px; }
        .search-box { width: 100%; padding: 15px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; margin-bottom: 20px; }
        .filter-buttons { margin-bottom: 20px; }
        .filter-buttons a { display: inline-block; padding: 8px 20px; margin-right: 10px; border-radius: 20px; text-decoration: none; }
        .filter-all { background: #3498db; color: white; }
        .filter-available { background: #27ae60; color: white; }
        .filter-taken { background: #e74c3c; color: white; }
        .dns-record { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #3498db; }
        .user-info { color: white; margin-right: 15px; }
    </style>
</head>
<body>
    <div class="navbar">
        <a href="/" class="brand">FreeDomain</a>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/domains">Domains</a>
            {% if current_user.is_authenticated %}
                <a href="/dashboard">Dashboard</a>
                {% if current_user.is_admin %}
                    <a href="/admin">Admin</a>
                {% endif %}
                <a href="/logout">Logout ({{ current_user.username }})</a>
            {% else %}
                <a href="/login">Login</a>
                <a href="/register">Register</a>
            {% endif %}
        </div>
    </div>
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""


@app.route("/")
def home():
    """Home page - Main landing page"""
    html = BASE_HTML.replace('{% block content %}{% endblock %}', """
        <div class="hero">
            <h1>FreeDomain - DigitalPlat</h1>
            <p>Free Domain For Everyone</p>
            <div style="margin-top: 30px;">
                <a href="/register" class="btn">Get Started</a>
                <a href="/domains" class="btn btn-primary">Browse Domains</a>
            </div>
        </div>
        <div class="features">
            <div class="feature">
                <h3>Free</h3>
                <p>No costs, completely free domains for everyone</p>
            </div>
            <div class="feature">
                <h3>Easy</h3>
                <p>Simple registration process in seconds</p>
            </div>
            <div class="feature">
                <h3>Fast</h3>
                <p>Instant domain activation and DNS setup</p>
            </div>
            <div class="feature">
                <h3>Secure</h3>
                <p>Your domains are safely stored and managed</p>
            </div>
        </div>
    """)
    return render_template_string(html, title="Home")


@app.route("/domains")
def domains():
    """Domains page - List available domains"""
    search_query = request.args.get('search', '').lower()
    filter_type = request.args.get('filter', 'all')

    filtered_domains = DOMAINS.copy()
    if search_query:
        filtered_domains = [d for d in filtered_domains if search_query in d['name'].lower()]
    if filter_type == 'available':
        filtered_domains = [d for d in filtered_domains if d['status'] == 'available']
    elif filter_type == 'taken':
        filtered_domains = [d for d in filtered_domains if d['status'] == 'taken']

    html = BASE_HTML.replace('{% block content %}{% endblock %}', """
        <h1>Available Domains</h1>
        <input type="text" class="search-box" placeholder="Search domains..." id="searchInput" value="{{ search_query }}">
        <div class="filter-buttons">
            <a href="/domains?filter=all" class="filter-all">All</a>
            <a href="/domains?filter=available" class="filter-available">Available</a>
            <a href="/domains?filter=taken" class="filter-taken">Taken</a>
        </div>
        <table>
            <tr>
                <th>Domain Name</th>
                <th>Status</th>
                <th>Price</th>
                <th>Registered</th>
                <th>Expires</th>
            </tr>
            {% for domain in domains %}
            <tr>
                <td>{{ domain.name }}</td>
                <td class="{{ domain.status }}">{{ domain.status }}</td>
                <td>{{ domain.price }}</td>
                <td>{{ domain.created_at or '-' }}</td>
                <td>{{ domain.expires_at or '-' }}</td>
            </tr>
            {% endfor %}
        </table>
        <script>
            document.getElementById('searchInput').addEventListener('keyup', function(e) {
                if(e.key === 'Enter') {
                    window.location.href = '/domains?search=' + this.value;
                }
            });
        </script>
    """)
    return render_template_string(html, title="Domains", domains=filtered_domains, search_query=search_query)


@app.route("/about")
def about():
    """About page - Project information"""
    html = BASE_HTML.replace('{% block content %}{% endblock %}', """
        <h1>About FreeDomain</h1>
        <p><strong>FreeDomain - DigitalPlat</strong> is a project dedicated to providing free domains for everyone.</p>
        <h2>Mission</h2>
        <p>Our mission is to make internet presence accessible to everyone, regardless of their financial situation.</p>
        <h2>Features</h2>
        <ul>
            <li>Free .free domain registration</li>
            <li>User accounts and dashboard</li>
            <li>DNS management</li>
            <li>Simple management interface</li>
            <li>Instant activation</li>
            <li>API access for developers</li>
        </ul>
        <h2>Contact</h2>
        <p>Email: support@freedomain.example</p>
    """)
    return render_template_string(html, title="About")


@app.route("/register", methods=["GET", "POST"])
def register_page():
    """User registration page"""
    global USER_COUNTER

    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    html_template = BASE_HTML.replace('{% block content %}{% endblock %}', """
        <h1>Create Account</h1>
        <p>Join FreeDomain to register and manage your free domains</p>
        <form method="POST">
            <div class="form-group">
                <label>Username</label>
                <input type="text" name="username" required placeholder="Choose a username">
            </div>
            <div class="form-group">
                <label>Email</label>
                <input type="email" name="email" required placeholder="Enter your email">
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" required placeholder="Choose a password">
            </div>
            <button type="submit" class="btn">Register</button>
            <a href="/login" class="btn btn-primary">Login</a>
        </form>
    """)

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not username or not email or not password:
            return render_template_string(html_template, title="Register", message="All fields are required", message_type="error")

        for user in USERS.values():
            if user.username == username:
                return render_template_string(html_template, title="Register", message="Username already exists", message_type="error")
            if user.email == email:
                return render_template_string(html_template, title="Register", message="Email already exists", message_type="error")

        password_hash = generate_password_hash(password)
        user = User(USER_COUNTER, username, email, password_hash)
        USERS[USER_COUNTER] = USER_COUNTER
        USER_COUNTER += 1

        # Reload the user
        user = User(USER_COUNTER - 1, username, email, password_hash)
        USERS[USER_COUNTER - 1] = user

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login_page'))

    return render_template_string(html_template, title="Register")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    """User login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    html_template = BASE_HTML.replace('{% block content %}{% endblock %}', """
        <h1>Login</h1>
        <p>Login to manage your domains</p>
        <form method="POST">
            <div class="form-group">
                <label>Username or Email</label>
                <input type="text" name="username" required placeholder="Enter username or email">
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" required placeholder="Enter password">
            </div>
            <button type="submit" class="btn">Login</button>
            <a href="/register" class="btn btn-primary">Register</a>
        </form>
    """)

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = None
        for u in USERS.values():
            if u.username == username or u.email == username:
                user = u
                break

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard'))

        return render_template_string(html_template, title="Login", message="Invalid credentials", message_type="error")

    return render_template_string(html_template, title="Login")


@app.route("/logout")
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@app.route("/dashboard")
@login_required
def dashboard():
    """User dashboard - Manage owned domains"""
    user_domains = [d for d in DOMAINS if d['owner_id'] == current_user.id]
    user_dns = {d['name']: DNS_RECORDS.get(d['name'], []) for d in user_domains}

    html = BASE_HTML.replace('{% block content %}{% endblock %}', """
        <h1>My Dashboard</h1>
        <p>Welcome, {{ current_user.username }}!</p>

        <h2>My Domains</h2>
        {% if domains %}
        <table>
            <tr>
                <th>Domain</th>
                <th>Status</th>
                <th>Created</th>
                <th>Expires</th>
                <th>Actions</th>
            </tr>
            {% for domain in domains %}
            <tr>
                <td>{{ domain.name }}</td>
                <td class="{{ domain.status }}">{{ domain.status }}</td>
                <td>{{ domain.created_at or '-' }}</td>
                <td>{{ domain.expires_at or '-' }}</td>
                <td>
                    <a href="/dns/{{ domain.name }}" class="btn btn-primary" style="padding: 5px 15px; font-size: 12px;">DNS</a>
                </td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p>You don't own any domains yet. <a href="/domains">Browse available domains</a></p>
        {% endif %}

        <h2>Register New Domain</h2>
        <form method="POST" action="/register/domain">
            <div class="form-group">
                <label>Choose a domain name:</label>
                <input type="text" name="domain" placeholder="Enter desired domain (e.g., mysite)" required>
            </div>
            <button type="submit" class="btn">Register Domain</button>
        </form>
    """)
    return render_template_string(html, title="Dashboard", domains=user_domains)


@app.route("/register/domain", methods=["POST"])
@login_required
def register_domain():
    """Register a domain for the logged in user"""
    domain_name = request.form.get("domain", "").strip().lower()

    if not domain_name:
        flash('Please enter a domain name', 'error')
        return redirect(url_for('dashboard'))

    # Validate domain name
    if not domain_name.replace('.', '').replace('-', '').isalnum():
        flash('Invalid domain name. Only letters, numbers, and hyphens allowed.', 'error')
        return redirect(url_for('dashboard'))

    full_domain = f"{domain_name}.free"

    # Check if domain exists
    domain_found = None
    for domain in DOMAINS:
        if domain['name'] == full_domain:
            domain_found = domain
            break

    if domain_found:
        if domain_found['status'] == 'taken':
            flash(f'Sorry, {full_domain} is already taken', 'error')
        else:
            # Register the domain
            domain_found['status'] = 'taken'
            domain_found['owner_id'] = current_user.id
            domain_found['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d')
            domain_found['expires_at'] = (datetime.datetime.now() + datetime.timedelta(days=365)).strftime('%Y-%m-%d')
            DNS_RECORDS[full_domain] = [
                {'type': 'A', 'value': '192.168.1.1', 'ttl': 3600},
                {'type': 'CNAME', 'value': 'www', 'ttl': 3600}
            ]
            flash(f'Success! {full_domain} is now registered to you!', 'success')
    else:
        # Create new domain
        new_domain = {
            "name": full_domain,
            "status": "taken",
            "price": "Free",
            "owner_id": current_user.id,
            "created_at": datetime.datetime.now().strftime('%Y-%m-%d'),
            "expires_at": (datetime.datetime.now() + datetime.timedelta(days=365)).strftime('%Y-%m-%d')
        }
        DOMAINS.append(new_domain)
        DNS_RECORDS[full_domain] = [
            {'type': 'A', 'value': '192.168.1.1', 'ttl': 3600},
            {'type': 'CNAME', 'value': 'www', 'ttl': 3600}
        ]
        flash(f'Success! {full_domain} is now registered to you!', 'success')

    return redirect(url_for('dashboard'))


@app.route("/dns/<domain_name>")
@login_required
def dns_management(domain_name):
    """DNS management page for a domain"""
    # Check if user owns the domain
    domain = None
    for d in DOMAINS:
        if d['name'] == domain_name:
            domain = d
            break

    if not domain or domain['owner_id'] != current_user.id:
        flash('You do not own this domain', 'error')
        return redirect(url_for('dashboard'))

    records = DNS_RECORDS.get(domain_name, [])

    html = BASE_HTML.replace('{% block content %}{% endblock %}', """
        <h1>DNS Management</h1>
        <h2>{{ domain_name }}</h2>

        <h3>DNS Records</h3>
        {% if records %}
        <table>
            <tr>
                <th>Type</th>
                <th>Value</th>
                <th>TTL</th>
            </tr>
            {% for record in records %}
            <tr>
                <td>{{ record.type }}</td>
                <td>{{ record.value }}</td>
                <td>{{ record.ttl }}</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p>No DNS records found</p>
        {% endif %}

        <h3>Add DNS Record</h3>
        <form method="POST" action="/dns/{{ domain_name }}/add">
            <div class="form-group">
                <label>Type</label>
                <select name="type">
                    <option value="A">A</option>
                    <option value="AAAA">AAAA</option>
                    <option value="CNAME">CNAME</option>
                    <option value="MX">MX</option>
                    <option value="TXT">TXT</option>
                </select>
            </div>
            <div class="form-group">
                <label>Value</label>
                <input type="text" name="value" required placeholder="e.g., 192.168.1.1">
            </div>
            <div class="form-group">
                <label>TTL</label>
                <input type="number" name="ttl" value="3600" required>
            </div>
            <button type="submit" class="btn">Add Record</button>
            <a href="/dashboard" class="btn btn-primary">Back</a>
        </form>
    """)
    return render_template_string(html, title="DNS Management", domain_name=domain_name, records=records)


@app.route("/dns/<domain_name>/add", methods=["POST"])
@login_required
def dns_add_record(domain_name):
    """Add DNS record for a domain"""
    # Check if user owns the domain
    domain = None
    for d in DOMAINS:
        if d['name'] == domain_name:
            domain = d
            break

    if not domain or domain['owner_id'] != current_user.id:
        flash('You do not own this domain', 'error')
        return redirect(url_for('dashboard'))

    record_type = request.form.get('type')
    value = request.form.get('value')
    ttl = int(request.form.get('ttl', 3600))

    if domain_name not in DNS_RECORDS:
        DNS_RECORDS[domain_name] = []

    DNS_RECORDS[domain_name].append({
        'type': record_type,
        'value': value,
        'ttl': ttl
    })

    flash(f'DNS record added successfully', 'success')
    return redirect(url_for('dns_management', domain_name=domain_name))


@app.route("/admin")
@login_required
def admin_panel():
    """Admin panel with statistics"""
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))

    total_domains = len(DOMAINS)
    available_domains = len([d for d in DOMAINS if d['status'] == 'available'])
    taken_domains = len([d for d in DOMAINS if d['status'] == 'taken'])
    total_users = len(USERS)

    html = BASE_HTML.replace('{% block content %}{% endblock %}', """
        <h1>Admin Panel</h1>

        <div class="stats">
            <div class="stat-card">
                <h2>{{ total_domains }}</h2>
                <p>Total Domains</p>
            </div>
            <div class="stat-card">
                <h2>{{ available_domains }}</h2>
                <p>Available</p>
            </div>
            <div class="stat-card">
                <h2>{{ taken_domains }}</h2>
                <p>Registered</p>
            </div>
            <div class="stat-card">
                <h2>{{ total_users }}</h2>
                <p>Users</p>
            </div>
        </div>

        <h2>All Domains</h2>
        <table>
            <tr>
                <th>Domain</th>
                <th>Status</th>
                <th>Owner ID</th>
                <th>Created</th>
                <th>Expires</th>
            </tr>
            {% for domain in domains %}
            <tr>
                <td>{{ domain.name }}</td>
                <td class="{{ domain.status }}">{{ domain.status }}</td>
                <td>{{ domain.owner_id or '-' }}</td>
                <td>{{ domain.created_at or '-' }}</td>
                <td>{{ domain.expires_at or '-' }}</td>
            </tr>
            {% endfor %}
        </table>

        <h2>All Users</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Username</th>
                <th>Email</th>
                <th>Admin</th>
            </tr>
            {% for user in users %}
            <tr>
                <td>{{ user.id }}</td>
                <td>{{ user.username }}</td>
                <td>{{ user.email }}</td>
                <td>{{ 'Yes' if user.is_admin else 'No' }}</td>
            </tr>
            {% endfor %}
        </table>
    """)
    return render_template_string(html, title="Admin Panel",
                                   total_domains=total_domains,
                                   available_domains=available_domains,
                                   taken_domains=taken_domains,
                                   total_users=total_users,
                                   domains=DOMAINS,
                                   users=list(USERS.values()))


@app.route("/api/domains")
def api_domains():
    """API endpoint - Return domains as JSON"""
    return jsonify({
        "success": True,
        "data": DOMAINS,
        "total": len(DOMAINS)
    })


@app.route("/api/domains/register", methods=["POST"])
def api_register_domain():
    """API endpoint to register a domain"""
    data = request.get_json()
    if not data or "domain" not in data:
        return jsonify({"success": False, "error": "Domain name required"}), 400
    domain_name = data["domain"].strip().lower()
    full_domain = f"{domain_name}.free"
    for domain in DOMAINS:
        if domain["name"] == full_domain:
            if domain["status"] == "taken":
                return jsonify({"success": False, "error": f"{full_domain} is already taken"}), 400
            domain["status"] = "taken"
            domain["price"] = "Registered"
            return jsonify({"success": True, "message": f"{full_domain} registered successfully", "domain": domain})
    new_domain = {"name": full_domain, "status": "taken", "price": "Registered", "owner_id": None, "created_at": None, "expires_at": None}
    DOMAINS.append(new_domain)
    return jsonify({"success": True, "message": f"{full_domain} registered successfully", "domain": new_domain})


@app.route("/api/users/register", methods=["POST"])
def api_register_user():
    """API endpoint to register a user"""
    global USER_COUNTER
    data = request.get_json()
    if not data or "username" not in data or "email" not in data or "password" not in data:
        return jsonify({"success": False, "error": "Username, email and password required"}), 400

    username = data["username"].strip()
    email = data["email"].strip()
    password = data["password"]

    for user in USERS.values():
        if user.username == username:
            return jsonify({"success": False, "error": "Username already exists"}), 400
        if user.email == email:
            return jsonify({"success": False, "error": "Email already exists"}), 400

    password_hash = generate_password_hash(password)
    user = User(USER_COUNTER, username, email, password_hash)
    USERS[USER_COUNTER] = user
    USER_COUNTER += 1

    return jsonify({"success": True, "message": "User registered successfully", "user_id": user.id})


@app.route("/api/stats")
def api_stats():
    """API endpoint for statistics"""
    return jsonify({
        "success": True,
        "stats": {
            "total_domains": len(DOMAINS),
            "available_domains": len([d for d in DOMAINS if d['status'] == 'available']),
            "taken_domains": len([d for d in DOMAINS if d['status'] == 'taken']),
            "total_users": len(USERS)
        }
    })


@app.route('/api/domains/batch', methods=['POST'])
def api_domains_batch():
    """Batch domain operations"""
    data = request.get_json() or {}
    operations = data.get('operations', [])
    
    results = []
    for op in operations:
        op_type = op.get('type')
        domain_name = op.get('domain')
        
        if op_type == 'check':
            domain = next((d for d in DOMAINS if d['name'] == domain_name), None)
            results.append({
                'domain': domain_name,
                'status': domain['status'] if domain else 'not_found'
            })
        elif op_type == 'register':
            domain = next((d for d in DOMAINS if d['name'] == domain_name), None)
            if domain and domain['status'] == 'available':
                domain['status'] = 'taken'
                domain['owner_id'] = op.get('owner_id', 1)
                domain['created_at'] = datetime.datetime.now().isoformat()
                results.append({'domain': domain_name, 'status': 'registered'})
            else:
                results.append({'domain': domain_name, 'status': 'failed', 'reason': 'not available'})
    
    return jsonify({
        'success': True,
        'results': results,
        'total': len(results)
    })


# Create admin user
admin_user = User(1, "admin", "admin@freedomain.example", generate_password_hash("admin123"), is_admin=True)
USERS[1] = admin_user
USER_COUNTER = 2

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
