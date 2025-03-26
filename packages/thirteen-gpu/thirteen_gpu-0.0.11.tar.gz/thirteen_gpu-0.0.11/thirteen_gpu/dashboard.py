import datetime
import json
import os
import subprocess
import multiprocessing  # multiprocessing 임포트

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse


app = FastAPI()


class WorkerData(BaseModel):
    user_id: str
    vast_ids: str


@app.post(
    "/add_worker"
)  # 기존의 @app.get("/add_worker")를 @app.post("/add_worker")로 변경
def add_worker(data: WorkerData):
    # 여기에 worker 추가 로직을 구현합니다.
    print(f"User ID: {data.user_id}, Vast IDs: {data.vast_ids}")

    for vast_id in data.vast_ids.split():
        os.system(f"python add_new_worker.py --vast_id {vast_id} --user {data.user_id}")
    return {"message": "Worker added successfully"}


class OwnerData(BaseModel):
    owner_id: str
    worker_id: str


@app.post("/set_owner")
def set_owner(data: OwnerData):
    try:
        print(f"{data=}")
        owner = data.owner_id
        worker_ids = data.worker_id.split()

        workers = json.loads(open("workers.json").read())
        for worker_id in worker_ids:
            if worker_id in workers:
                workers[worker_id]["owner"] = owner
            else:
                raise HTTPException(
                    status_code=404, detail=f"Worker ID {worker_id} not found"
                )

        with open("workers.json", "w") as f:
            json.dump(workers, f, indent=4)

        # owner 변경 이력을 디스크에 저장
        with open("owner_change_log.txt", "a") as log_file:
            log_file.write(
                f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Owner 변경: {worker_ids} -> {owner}\n"
            )

        os.system("pkill -f run_scheduler.py")
        return {"message": "Owner 가 성공적으로 설정되었습니다."}
    except Exception as e:
        print(f"{e=}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/show_owner_change_log")
def show_owner_change_log():
    if not os.path.exists("owner_change_log.txt"):
        return "No owner change log"

    with open("owner_change_log.txt", "r") as log_file:
        log_lines = log_file.readlines()
        log_lines.reverse()
        log_content = "<br>".join(line.replace('"', "") for line in log_lines)
        log_content = log_content.replace("\n", "")
        log_content = log_content.replace("seilna", '<span style="color:red;">seilna</span>')
        log_content = log_content.replace("forybm", '<span style="color:green;">forybm</span>')
        log_content = log_content.replace("joohong", '<span style="color:blue;">joohong</span>')
        log_content = log_content.replace("lynch", '<span style="color:purple;">lynch</span>')
    return log_content


@app.post("/vast_on")
def vast_on():
    instances = json.loads(
        subprocess.check_output("vast show instances --raw", shell=True)
    )

    for instance in instances:
        if instance["actual_status"] == "exited":
            os.system(f"vast start instance {instance['id']}")

            print(f"Starting instance {instance['id']}")

    return {"message": "Turn on Done"}


@app.post("/vast_off")
def vast_off():
    instances = json.loads(
        subprocess.check_output("vast show instances --raw", shell=True)
    )

    for instance in instances:
        if instance["actual_status"] == "running":
            os.system(f"vast stop instance {instance['id']}")

            print(f"Stopping instance {instance['id']}")

    # show popup
    return {"message": "Turn off Done"}


@app.post("/vast_stop_schedule")
async def vast_stop_schedule():
    instances = json.loads(
        subprocess.check_output("vast show instances --raw", shell=True)
    )

    for instance in instances:
        if instance["actual_status"] == "exited":
            os.system(f"vast stop instance {instance['id']}")

            print(f"Stopping instance {instance['id']}")
    return {"message": "Stop Schduling Done"}


@app.post("/set_owner")
def set_owner():
    try:
        # 여기에 소유자 설정 로직을 구현합니다.
        # 예를 들어, 데이터베이스에 소유자 정보를 업데이트하는 코드가 있을 수 있니다.
        print("Owner has been set successfully.")
        return {"message": "Owner set successfully"}
    except Exception as e:
        print(f"Error setting owner: {e}")
        raise HTTPException(status_code=500, detail="Failed to set owner")


class ProjectData(BaseModel):
    project_name: str
    user: str


@app.post("/delete_project")
def delete_project(data: ProjectData):
    project_path = f"/home/seilna/tmux_workspace/{data.project_name}"

    if not os.path.exists(project_path):
        raise HTTPException(status_code=404, detail=f"프로젝트 폴더 {data.project_name}가 존재하지 않습니다.")

    try:
        os.system(f"rm -rf {project_path}")
        return {"message": f"프로젝트 {data.project_name} 폴더가 성공적으로 삭제되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"폴더 삭제 중 오류가 발생했습니다: {e}")

# 아래 worker에서 파일 삭제 작업을 병렬로 실행하기 위한 별도 함수
def process_worker(args):
    worker_id, project = args
    remote_command = (
        "bash -c '"
        "count=0; "
        "deleted=\"\"; "
        "for f in /home/thirteen/{project}/*.status; do "
            "if [ -f \"$f\" ]; then "
                "if grep -q failed \"$f\"; then "
                    "rm -f \"$f\"; "
                    "deleted=\"$deleted|$f\"; "
                    "count=$((count+1)); "
                "fi; "
            "fi; "
        "done; "
        "echo \"$count|||$deleted\"'"
    ).format(project=project)
    
    try:
        output = subprocess.check_output(
            ["ssh", "-o", "BatchMode=yes", f"{worker_id}", remote_command],
            stderr=subprocess.STDOUT
        )
        output_str = output.decode().strip()
        output_str = output_str.split("fun!\n")[-1]
        if "|||" in output_str:
            count_part, deleted_part = output_str.split("|||", 1)
        else:
            count_part, deleted_part = output_str, ""
        removed = int(count_part)
        files_deleted = [f for f in deleted_part.split("|") if f.strip() != ""]
        return (worker_id, {"removed": removed, "files": files_deleted})
    except subprocess.CalledProcessError as e:
        error_msg = e.output.decode()
        # 비밀번호가 요구되면 스킵하도록 처리
        if "password" in error_msg.lower() or "permission denied" in error_msg.lower():
            return (worker_id, {"skipped": "비밀번호 요구로 인해 스킵됨"})
        return (worker_id, {"error": error_msg})
    except Exception as e:
        return (worker_id, {"error": str(e)})

@app.post("/rerun_failed_jobs")
def rerun_failed_jobs(data: ProjectData):
    project_name = data.project_name
    user = data.user
    
    workers = json.loads(open("worker_pool_names.txt").read())
    worker_ids = workers[user]

    total_removed = 0
    details = {}

    # worker id와 프로젝트 이름을 tuple로 구성
    worker_list = [(worker_id, project_name) for worker_id in worker_ids]

    # multiprocessing을 사용해 각 worker에 대해 병렬 실행
    print(f"failed job 의 status 파일 삭제 시작")
    with multiprocessing.Pool() as pool:
        results = pool.map(process_worker, worker_list)

    for worker_id, result in results:
        if "removed" in result:
            total_removed += result["removed"]
            details[worker_id] = result
            print(f"Worker {worker_id}: 삭제된 파일 수 {result['removed']}, 파일 목록: {result.get('files', [])}")
        else:
            details[worker_id] = result
            print(f"Worker {worker_id} 작업 중 오류 발생: {result.get('error')}")

    return {
        "message": f"모든 remote worker에서 실패한 상태 파일 총 {total_removed}개 삭제됨",
        "details": details
    }

@app.get("/")
def read_root():

    scheduler_off = False

    worker_pool_names = open("worker_pool_names.txt").read()
    available_job_slots = open("available_job_slots.txt").read().strip()

    # get last update time of `status.json`
    last_update = os.path.getmtime("status.json")
    last_update = datetime.datetime.fromtimestamp(last_update) + datetime.timedelta(
        hours=9
    )

    # if `last_update` not updated for 1 hour, set it to `None`
    if datetime.datetime.now() + datetime.timedelta(
        hours=9
    ) - last_update > datetime.timedelta(minutes=5):
        scheduler_off = True

    last_update_before = (
        datetime.datetime.now() + datetime.timedelta(hours=9) - last_update
    )
    last_update = last_update.strftime("%Y-%m-%d %H:%M:%S")

    status = json.load(open("status.json"))
    text = "<a href='http://54.180.160.135:2014/'>GPU Status</a> <br>"
    text += "<a href='http://54.180.160.135:2015'>Task 현황</a> <br>"
    # Before ss.mm seconds format
    # microseconds
    if scheduler_off:
        text += f"<h3> Scheduler is off, Last Update: Before {last_update_before.seconds}.{str(last_update_before.microseconds)[:2]} seconds </h3>"
    else:
        text += f"<h3> Last Update: Before {last_update_before.seconds}.{str(last_update_before.microseconds)[:2]} seconds </h3>"

    text += f"<h3> Active Workers : {worker_pool_names} </h3>"
    text += f"<h3> Job Slots: {available_job_slots} </h3>"

    projects = []
    for project_name, project_status in status.items():
        user = project_status["user"]
        submit_at = project_status["submit_at"]

        status_info = [(status_name, status_count) for status_name, status_count in project_status["status"].items()]

        projects.append((project_name, user, submit_at, status_info))

    projects = sorted(projects, key=lambda x: x[2], reverse=True)

    for project_name, user, submit_at, status_info in projects:
        text += f"""
            <h2> Project: {project_name} </h2>
        """
        text += f"user: {user} / submitted at: {submit_at} <br>"

        for status_name, status_count in status_info:
            text += f" {status_name}: {status_count} "
            
        # Delete 버튼 추가 및 Rerun Failed Jobs 버튼 오른쪽에 배치
        text += f"""
            <br>
            <button onclick="deleteProject('{project_name}', '{user}')">Delete</button>
            <button onclick="rerunFailedJobs('{project_name}', '{user}')">Rerun Failed Jobs</button>
        """ 

    if len(projects) == 0:
        text += "No projects"

    # JavaScript 함수 구현 (deleteProject와 rerunFailedJobs)
    text += """
        <script>
        function deleteProject(projectName, user) {
            if (confirm(projectName + " 프로젝트를 정말 삭제하시겠습니까?")) {
                fetch('/delete_project', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ 'project_name': projectName, 'user': user })
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    // 페이지를 새로고침
                    location.reload();
                })
                .catch(error => {
                    alert("삭제 중 오류가 발생했습니다.");
                    console.error(error);
                });
            }
        }
        function rerunFailedJobs(projectName, user) {
            if (confirm(projectName + " 프로젝트의 실패한 작업들을 재실행하시겠습니까?")) {
                fetch('/rerun_failed_jobs', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ 'project_name': projectName, 'user': user })
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    // 페이지를 새로고침
                    location.reload();
                })
                .catch(error => {
                    alert("실패한 작업 재실행 도중 오류가 발생했습니다.");
                    console.error(error);
                });
            }
        }
        </script>
    """

    # contents = html.format(content=text)
    html = open("dashboard.html").read()
    contents = html.replace("PLACEHOLDER", text)

    # return HTML Rendered Page
    return HTMLResponse(content=contents, status_code=200)
