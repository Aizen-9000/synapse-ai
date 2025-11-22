import os
import uuid
import shutil
from docker import DockerClient
from typing import Optional

# Load sandbox settings from environment variables
SANDBOX_TIMEOUT = int(os.getenv("SANDBOX_TIMEOUT", 10))
SANDBOX_IMAGE = os.getenv("SANDBOX_IMAGE", "python:3.10-slim")

# Docker client
client = DockerClient(base_url="unix://var/run/docker.sock")


async def run_user_script(user_id: str, script_text: str, timeout: Optional[int] = None):
    """
    Runs untrusted user Python code inside a restricted Docker container.
    """
    timeout = timeout or SANDBOX_TIMEOUT

    # Create secure temporary workspace
    workdir = f"/tmp/sandbox_{user_id}_{uuid.uuid4().hex}"
    os.makedirs(workdir, exist_ok=True)
    script_path = os.path.join(workdir, "user_script.py")

    # Write script to file
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_text)

    # Run container safely
    try:
        container = client.containers.run(
            SANDBOX_IMAGE,
            command=["python", "/workspace/user_script.py"],
            volumes={workdir: {"bind": "/workspace", "mode": "ro"}},
            detach=True,
            network_disabled=True,
            mem_limit="256m",
            cpu_period=100000,
            cpu_quota=50000,
            stderr=True,
            stdout=True,
        )
    except Exception as e:
        shutil.rmtree(workdir, ignore_errors=True)
        return {"error": str(e)}

    # Collect results
    try:
        result = container.wait(timeout=timeout)
        logs = container.logs(stdout=True, stderr=True)
        out = logs.decode(errors="ignore")

    except Exception as e:
        # Kill container if timeout
        try:
            container.kill()
        except:
            pass
        out = f"[TIMEOUT/ERROR] {e}"

    finally:
        # Clean up container + workspace
        try:
            container.remove(force=True)
        except:
            pass

        shutil.rmtree(workdir, ignore_errors=True)

    return {"output": out}