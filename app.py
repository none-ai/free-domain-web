from flask import Flask, jsonify, render_template_string

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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
