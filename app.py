from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# Sample domain data
DOMAINS = [
    {"name": "example.free", "status": "available", "price": "Free"},
    {"name": "mydomain.free", "status": "available", "price": "Free"},
    {"name": "testsite.free", "status": "taken", "price": "N/A"},
]


@app.route("/")
def home():
    """Home page - Main landing page"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FreeDomain - DigitalPlat</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            h1 { color: #2c3e50; }
            .nav { margin: 20px 0; }
            .nav a { margin-right: 20px; color: #3498db; text-decoration: none; }
            .nav a:hover { text-decoration: underline; }
            .hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; border-radius: 10px; text-align: center; }
            .features { display: flex; gap: 20px; margin-top: 30px; }
            .feature { flex: 1; padding: 20px; background: #ecf0f1; border-radius: 8px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>FreeDomain - DigitalPlat</h1>
            <h2>Free Domain For Everyone</h2>
            <div class="nav">
                <a href="/">Home</a>
                <a href="/domains">Domains</a>
                <a href="/about">About</a>
                <a href="/register">Register</a>
                <a href="/api/domains">API</a>
            </div>
            <div class="hero">
                <h3>Get Your Free Domain Today!</h3>
                <p>Simple. Free. For Everyone.</p>
            </div>
            <div class="features">
                <div class="feature">
                    <h4>Free</h4>
                    <p>No costs, completely free domains</p>
                </div>
                <div class="feature">
                    <h4>Easy</h4>
                    <p>Simple registration process</p>
                </div>
                <div class="feature">
                    <h4>Fast</h4>
                    <p>Instant domain activation</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route("/domains")
def domains():
    """Domains page - List available domains"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Domains - FreeDomain</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            .nav { margin-bottom: 20px; }
            .nav a { margin-right: 20px; color: #3498db; text-decoration: none; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background: #3498db; color: white; }
            .available { color: #27ae60; font-weight: bold; }
            .taken { color: #e74c3c; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="nav">
                <a href="/">Home</a>
                <a href="/domains">Domains</a>
                <a href="/about">About</a>
                <a href="/register">Register</a>
                <a href="/api/domains">API</a>
            </div>
            <h1>Available Domains</h1>
            <table>
                <tr>
                    <th>Domain Name</th>
                    <th>Status</th>
                    <th>Price</th>
                </tr>
                {% for domain in domains %}
                <tr>
                    <td>{{ domain.name }}</td>
                    <td class="{{ domain.status }}">{{ domain.status }}</td>
                    <td>{{ domain.price }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, domains=DOMAINS)


@app.route("/about")
def about():
    """About page - Project information"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>About - FreeDomain</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            .nav { margin-bottom: 20px; }
            .nav a { margin-right: 20px; color: #3498db; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="nav">
                <a href="/">Home</a>
                <a href="/domains">Domains</a>
                <a href="/about">About</a>
                <a href="/register">Register</a>
                <a href="/api/domains">API</a>
            </div>
            <h1>About FreeDomain</h1>
            <p><strong>FreeDomain - DigitalPlat</strong> is a project dedicated to providing free domains for everyone.</p>
            <h2>Mission</h2>
            <p>Our mission is to make internet presence accessible to everyone, regardless of their financial situation.</p>
            <h2>Features</h2>
            <ul>
                <li>Free .free domain registration</li>
                <li>Simple management interface</li>
                <li>Instant activation</li>
                <li>API access for developers</li>
            </ul>
            <h2>Contact</h2>
            <p>Email: support@freedomain.example</p>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route("/api/domains")
def api_domains():
    """API endpoint - Return domains as JSON"""
    return jsonify({
        "success": True,
        "data": DOMAINS,
        "total": len(DOMAINS)
    })


@app.route("/register", methods=["GET", "POST"])
def register():
    """Domain registration page"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Register Domain - FreeDomain</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 500px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            .nav { margin-bottom: 20px; }
            .nav a { margin-right: 20px; color: #3498db; text-decoration: none; }
            input { width: 100%; padding: 10px; margin: 10px 0; box-sizing: border-box; }
            button { width: 100%; padding: 12px; background: #27ae60; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #219150; }
            .message { padding: 15px; margin: 10px 0; border-radius: 5px; }
            .success { background: #d4edda; color: #155724; }
            .error { background: #f8d7da; color: #721c24; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="nav">
                <a href="/">Home</a>
                <a href="/domains">Domains</a>
                <a href="/about">About</a>
                <a href="/register">Register</a>
            </div>
            <h1>Register Your Free Domain</h1>
            {% if message %}
            <div class="message {{ message_type }}">{{ message }}</div>
            {% endif %}
            <form method="POST">
                <label>Choose a domain name:</label>
                <input type="text" name="domain" placeholder="Enter desired domain (e.g., mysite)" required>
                <button type="submit">Register Domain</button>
            </form>
            <p><small>Your domain will be: [name].free</small></p>
        </div>
    </body>
    </html>
    """
    if request.method == "POST":
        domain_name = request.form.get("domain", "").strip().lower()
        if not domain_name:
            return render_template_string(html, message="Please enter a domain name", message_type="error")
        full_domain = f"{domain_name}.free"
        for domain in DOMAINS:
            if domain["name"] == full_domain:
                if domain["status"] == "taken":
                    return render_template_string(html, message=f"Sorry, {full_domain} is already taken", message_type="error")
                else:
                    domain["status"] = "taken"
                    domain["price"] = "Registered"
                    return render_template_string(html, message=f"Success! {full_domain} is now registered to you!", message_type="success")
        DOMAINS.append({"name": full_domain, "status": "taken", "price": "Registered"})
        return render_template_string(html, message=f"Success! {full_domain} is now registered to you!", message_type="success")
    return render_template_string(html)


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
    new_domain = {"name": full_domain, "status": "taken", "price": "Registered"}
    DOMAINS.append(new_domain)
    return jsonify({"success": True, "message": f"{full_domain} registered successfully", "domain": new_domain})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
