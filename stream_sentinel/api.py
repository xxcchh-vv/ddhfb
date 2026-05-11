from pathlib import Path

from flask import Flask, jsonify, request

from config import load_config, save_config
from job_controller import job_controller
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


@app.route('/api/jobs/stop', methods=['POST'])
def stop_job():
    payload = request.json or {}
    name = payload.get('name')

    if not name:
        return jsonify({'error': 'missing name'}), 400

    job_controller.stop(name)
    runtime_registry.set_state(name, 'stopped')

    return jsonify({'success': True, 'name': name})


@app.route('/api/config')
def get_config():
    return jsonify(load_config())


@app.route('/api/config', methods=['POST'])
def update_config():
    config = request.json
    save_config(config)
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
