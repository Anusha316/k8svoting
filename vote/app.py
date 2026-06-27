from flask import Flask, request, render_template_string
import redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Vote!</title>
    <style>
        body { font-family: Arial; display: flex; justify-content: center; align-items: center;
               min-height: 100vh; margin: 0; background: #1a1a2e; color: white; }
        .container { text-align: center; }
        h1 { font-size: 3em; }
        .buttons { display: flex; gap: 40px; justify-content: center; margin-top: 20px; }
        button { padding: 30px 60px; font-size: 2em; border: none; border-radius: 15px; cursor: pointer; }
        .cat { background: #e94560; color: white; }
        .dog { background: #0f3460; color: white; }
        .msg { margin-top: 30px; font-size: 1.5em; color: #a8ff78; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐱 vs 🐶</h1>
        <div class="buttons">
            <form method="POST" action="/vote">
                <button class="cat" name="vote" value="cat">🐱 Cat</button>
            </form>
            <form method="POST" action="/vote">
                <button class="dog" name="vote" value="dog">🐶 Dog</button>
            </form>
        </div>
        {% if msg %}<p class="msg">{{ msg }}</p>{% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML, msg=None)

@app.route('/vote', methods=['POST'])
def vote():
    choice = request.form.get('vote')
    if choice in ['cat', 'dog']:
        r.incr(choice)
    return render_template_string(HTML, msg=f"You voted for {choice}! ✅")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
