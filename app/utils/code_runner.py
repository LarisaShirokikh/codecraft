import docker
import tempfile

def execute_code(code: str) -> dict:
    client = docker.from_env()
    
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w") as temp_file:
        temp_file.write(code)
        temp_file.flush()
        
        try:
            # Запуск кода в изолированном контейнере
            logs = client.containers.run(
                "python:3.9-slim",
                f"python {temp_file.name}",
                remove=True,
                timeout=10,
                network_disabled=True  # Отключаем доступ к сети
            )
            return {"output": logs.decode(), "success": True}
        except docker.errors.ContainerError as e:
            return {"output": str(e.stderr.decode()), "success": False}