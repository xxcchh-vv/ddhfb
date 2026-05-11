from pathlib import Path

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

    html = ['<h1>Stream Sentinel Dashboard</h1>']

    html.append('<h2>Recent Jobs</h2>')
    html.append('<table border="1" cellpadding="6">')
    html.append('<tr><th>Job</th><th>Status</th><th>Started</th><th>Finished</th></tr>')

    for row in rows:
        html.append(
            f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>'
        )

    html.append('</table>')

    html.append('<h2>Logs</h2>')

    log_dir = Path('./logs')

    if log_dir.exists():
        for log_file in sorted(log_dir.glob('*.log')):
            html.append(f'<h3>{log_file.name}</h3>')
            html.append('<pre>')
            html.append(log_file.read_text(encoding='utf-8')[-4000:])
            html.append('</pre>')

    return ''.join(html)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
