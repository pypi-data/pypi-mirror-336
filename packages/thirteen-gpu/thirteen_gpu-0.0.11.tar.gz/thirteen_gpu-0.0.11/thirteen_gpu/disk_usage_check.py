import os
from datetime import datetime
from time import sleep


while True:
    with open("thirteen_gpu/worker_pool_names.txt", "r") as f:
        workers = f.read().strip().split(" ")

    last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    usage_result = f""
    for worker in workers:
        result = os.popen(f"ssh {worker} 'df -h'").read()

        for r in result.split("\n"):
            usage = r.strip().split()
            if usage[-1] == "/":
                print(worker, usage[-3])
                usage_result += f"{worker}: {usage[-3]} / "
                break

    with open("thirteen_gpu/worker_disk_usage.txt", "w") as f:
        f.write(usage_result)

    sleep(3600)
