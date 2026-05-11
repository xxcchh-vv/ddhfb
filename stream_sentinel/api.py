from pathlib import Path

from flask import Flask, jsonify

from runtime import runtime_registry

app = Flask(__name__)


@app.route('/api/jobs')
def jobs():
    return jsonify(runtime_registry.list_jobs())


@app.route('/api/logs')
def logs():
    output = {}

    log_dir = Path('./logs')

    if log_dir.exists():
        for log_file in log_dir.glob('*.log'):
            output[log_file.name] = log_file.read_text(encoding='utf-8')[-2000:]

    return jsonify(output)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
