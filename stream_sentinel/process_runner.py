import subprocess
from pathlib import Path

from runtime import runtime_registry


class ProcessRunner:
    @staticmethod
    def run(job_name: str, args: list[str], log_file: str | None = None) -> int:
        stdout = None
        stderr = None
        handle = None

        if log_file:
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)
            handle = open(log_file, 'a', encoding='utf-8')
            stdout = handle
            stderr = handle

        process = subprocess.Popen(args, stdout=stdout, stderr=stderr)
        runtime_registry.ensure(job_name).process = process

        try:
            return process.wait()
        finally:
            runtime_registry.ensure(job_name).process = None
            if handle:
                handle.close()
