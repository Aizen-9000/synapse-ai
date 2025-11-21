import os
import uuid
import shutil
from docker import DockerClient
from .config import settings
from typing import Optional

# WARNING: Running user code is inherently dangerous. This example shows the mechanics only. Use heavy hardening in real products.
client = DockerClient(base_url="unix://var/run/docker.sock")

async def run_user_script(user_id: str, script_text: str, timeout: Optional[int] = None):
    timeout = timeout or settings.SANDBOX_TIMEOUT
    workdir = f"/tmp/sandbox_{user_id}_{uuid.uuid4().hex}"
    os.makedirs(workdir, exist_ok=True)
    script_path = os.path.join(workdir, "user_script.py")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_text)

    # Run container: read-only workspace + limited resources
    try:
        container = client.containers.run(
            settings.SANDBOX_IMAGE,
            command=["python", "/workspace/user_script.py"],
            volumes={workdir: {'bind': '/workspace', 'mode': 'ro'}},
            detach=True,
            network_disabled=True,
            mem_limit='256m',
            cpu_period=100000,
            cpu_quota=50000,
            stderr=True,
            stdout=True,
        )
    except Exception as e:
        shutil.rmtree(workdir, ignore_errors=True)
        return {'error': str(e)}

    try:
        result = container.wait(timeout=timeout)
        logs = container.logs(stdout=True, stderr=True)
        out = logs.decode(errors='ignore')
    except Exception as e:
        try:
            container.kill()
        except Exception:
            pass
        out = f"[TIMEOUT/ERROR] {e}"
    finally:
        try:
            container.remove(force=True)
        except Exception:
            pass
        shutil.rmtree(workdir, ignore_errors=True)
    return {'output': out}

