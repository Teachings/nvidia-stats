# server.py
import subprocess
import re
import psutil
from fastapi import FastAPI

app = FastAPI()

def get_gpu_stats():
    result = subprocess.run(["nvidia-smi", "--query-gpu=name,utilization.gpu,memory.used,memory.total", "--format=csv,noheader,nounits"],
                            stdout=subprocess.PIPE, text=True)
    gpus = result.stdout.strip().split('\n')
    gpu_stats = []
    
    for gpu in gpus:
        name, utilization, memory_used, memory_total = re.findall(r'[\w\s]+|\d+', gpu)
        gpu_stats.append({
            "name": name.strip(),
            "utilization": f"{utilization}%",
            "memory_used": f"{memory_used} MiB",
            "memory_total": f"{memory_total} MiB"
        })
    
    return gpu_stats

def get_cpu_stats():
    return {
        "cpu_utilization": f"{psutil.cpu_percent(interval=1)}%"
    }

def get_ram_stats():
    ram = psutil.virtual_memory()
    return {
        "ram_used": f"{ram.used // (1024 * 1024)} MiB",
        "ram_total": f"{ram.total // (1024 * 1024)} MiB",
        "ram_utilization": f"{ram.percent}%"
    }

@app.get("/system_stats")
async def system_stats():
    try:
        gpu_stats = get_gpu_stats()
        cpu_stats = get_cpu_stats()
        ram_stats = get_ram_stats()
        
        return {
            "gpu_stats": gpu_stats,
            "cpu_stats": cpu_stats,
            "ram_stats": ram_stats
        }
    except Exception as e:
        return {"error": str(e)}
