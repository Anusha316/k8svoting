from flask import Flask, render_template_string
import psycopg2

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Results</title>
    <meta http-equiv="refresh" content="2">
    <style>
        body { font-family: Arial; display: flex; justify-content: center; align-items: center;
               min-height: 100vh; margin: 0; background: #1a1a2e; color: white; }
        .container { text-align: center; width: 500px; }
        .bar-bg { background: rgba(255,255,255,0.1); border-radius: 10px; height: 40px; margin: 10px 0; }
        .bar { height: 100%; border-radius: 10px; display: flex; align-items: center; padding-left: 10px; }
        .cat-bar { background: #e94560; }
        .dog-bar { background: #0f3460; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Results</h1>
        <p>Total Votes: {{ total }}</p>
        <p>🐱 Cat - {{ cat_votes }} votes</p>
        <div class="bar-bg"><div class="bar cat-bar" style="width: {{ cat_pct }}%">{{ cat_pct }}%</div></div>
        <p>🐶 Dog - {{ dog_votes }} votes</p>
        <div class="bar-bg"><div class="bar dog-bar" style="width: {{ dog_pct }}%">{{ dog_pct }}%</div></div>
    </div>
</body>
</html>
"""

def get_results():
    try:
        conn = psycopg2.connect(host="postgres", database="votes", user="postgres", password="password")
        cur = conn.cursor()
        cur.execute("SELECT vote, COUNT(*) FROM votes GROUP BY vote")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        results = {'cat': 0, 'dog': 0}
        for row in rows:
            results[row[0]] = row[1]
        return results
    except:
        return {'cat': 0, 'dog': 0}

@app.route('/')
def index():
    results = get_results()
    cat_votes = results['cat']
    dog_votes = results['dog']
    total = cat_votes + dog_votes
    cat_pct = round((cat_votes / total * 100) if total > 0 else 0)
    dog_pct = round((dog_votes / total * 100) if total > 0 else 0)
    return render_template_string(HTML, cat_votes=cat_votes, dog_votes=dog_votes,
                                   total=total, cat_pct=cat_pct, dog_pct=dog_pct)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
