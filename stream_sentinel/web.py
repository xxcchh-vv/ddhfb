from flask import Flask
from database import Database

app = Flask(__name__)
db = Database()


@app.route('/')
def index():
    conn = db.connect()
    rows = conn.execute(
        'SELECT job_name, status, started_at, finished_at FROM job_runs ORDER BY id DESC LIMIT 50'
    ).fetchall()

    html = ['<h1>Stream Sentinel</h1>']
    html.append('<table border="1" cellpadding="6">')
    html.append('<tr><th>Job</th><th>Status</th><th>Started</th><th>Finished</th></tr>')

    for row in rows:
        html.append(
            f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>'
        )

    html.append('</table>')
    return ''.join(html)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
