import requests
import os
import json
import shutil
import time
import subprocess
import glob
import sys

# 설정
BASE_URL = "http://127.0.0.1:7860"
API_PREFIX = "/gradio_api"
SPEED_RATE = 1.2

# 프로젝트 루트 및 레퍼런스 설정
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "..", ".."))
REF_AUDIO_PATH = os.path.join(PROJECT_ROOT, "reference_voice.mp3")
REF_TEXT = "안녕하세요 여러분. 반갑습니다. 오늘도 저희 채널을 찾아주셔서 감사합니다. 영상이 도움되셨다면 구독과 좋아요를 눌러주세요."

def upload_file(file_path):
    url = f"{BASE_URL}{API_PREFIX}/upload"
    with open(file_path, "rb") as f:
        files = {"files": f}
        response = requests.post(url, files=files)
    if response.status_code == 200:
        result = response.json()
        path = result[0]
        return {"path": path, "meta": {"_type": "gradio.FileData"}}
    else:
        raise Exception(f"파일 업로드 실패: {response.text}")

def call_api(api_name, data):
    url = f"{BASE_URL}{API_PREFIX}/call{api_name}"
    payload = {"data": data}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()["event_id"]
    else:
        raise Exception(f"API 호출 시작 실패 ({api_name}): {response.text}")

def get_result(api_name, event_id):
    url = f"{BASE_URL}{API_PREFIX}/call{api_name}/{event_id}"
    response = requests.get(url, stream=True)
    current_event = None
    for line in response.iter_lines():
        if line:
            line_str = line.decode('utf-8').strip()
            if line_str.startswith("event:"):
                current_event = line_str[6:].strip()
            elif line_str.startswith("data:"):
                data_str = line_str[5:].strip()
                if current_event == "complete":
                    return json.loads(data_str)
                if current_event == "error":
                    raise Exception(f"API 에러 이벤트: {data_str}")
    raise Exception("결과를 찾지 못했습니다.")

def change_speed(input_file, output_file, rate=SPEED_RATE):
    cmd = ["ffmpeg", "-i", input_file, "-filter:a", f"atempo={rate}", output_file, "-y"]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    outputs_dir = os.path.join(PROJECT_ROOT, "outputs")
    folder_path = None

    if len(sys.argv) >= 2:
        arg_path = sys.argv[1]
        # 1. 입력한 경로가 그대로 존재하는 경우
        if os.path.exists(arg_path):
            folder_path = arg_path
        # 2. outputs/<arg_path> 형태로 존재하는 경우
        elif os.path.exists(os.path.join(outputs_dir, arg_path)):
            folder_path = os.path.join(outputs_dir, arg_path)
        else:
            print(f"에러: 지정한 폴더를 찾을 수 없습니다: {arg_path}")
            return
    else:
        # 인자가 없는 경우, outputs/ 디렉토리 내의 하위 폴더 자동 스캔
        if not os.path.exists(outputs_dir):
            print("에러: outputs 디렉토리가 존재하지 않습니다.")
            return
            
        subdirs = [os.path.join(outputs_dir, d) for d in os.listdir(outputs_dir) if os.path.isdir(os.path.join(outputs_dir, d))]
        
        # .md 파일이 존재하고 output_1.2x.wav 파일이 존재하지 않는 폴더 목록 필터링
        target_dirs = []
        for sd in subdirs:
            md_files = glob.glob(os.path.join(sd, "*.md"))
            has_output = os.path.exists(os.path.join(sd, "output_1.2x.wav"))
            if md_files and not has_output:
                target_dirs.append(sd)
                
        if not target_dirs:
            # 만약 조건에 맞는 폴더가 없다면, 그냥 outputs 폴더 내에서 가장 최근에 수정된 폴더를 탐색
            if subdirs:
                # 수정 시간 기준 정렬
                subdirs.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                folder_path = subdirs[0]
                print(f"[*] 미처리 폴더가 없어 가장 최근 수정된 폴더를 선택했습니다: {folder_path}")
            else:
                print("사용법: python3 generate.py <폴더경로>")
                print("또는 outputs/ 폴더 내에 하위 폴더와 .md 파일을 생성한 후 인자 없이 실행하세요.")
                return
        else:
            # 미처리 폴더 중 가장 최근 수정된 폴더 선택
            target_dirs.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            folder_path = target_dirs[0]
            print(f"[*] 자동으로 처리할 최신 미처리 폴더를 탐색했습니다: {folder_path}")

    # MD 파일 탐색 (script.md 최우선 탐색)
    script_path = None
    priority_names = ["script.md", "대본.md"]
    for name in priority_names:
        candidate = os.path.join(folder_path, name)
        if os.path.exists(candidate):
            script_path = candidate
            break
            
    if not script_path:
        # *script*.md 패턴 탐색
        script_candidates = glob.glob(os.path.join(folder_path, "*script*.md")) + glob.glob(os.path.join(folder_path, "*대본*.md"))
        if script_candidates:
            script_path = script_candidates[0]
            
    if not script_path:
        md_files = glob.glob(os.path.join(folder_path, "*.md"))
        # asset_sheet.md, plan.md, prompts.md, publish_kit.md 등 대본이 아닌 파일 제외
        non_script = ["asset_sheet.md", "plan.md", "prompts.md", "publish_kit.md", "README.md"]
        filtered = [f for f in md_files if os.path.basename(f) not in non_script]
        if filtered:
            script_path = filtered[0]
        elif md_files:
            script_path = md_files[0]

    if not script_path:
        print(f"에러: {folder_path} 내에 대본 MD 파일이 없습니다.")
        return
    
    print(f"[*] 대본 파일 선택됨: {script_path}")
    with open(script_path, 'r', encoding='utf-8') as f:
        script_text = f.read()

    print(f"[*] 처리 시작: {folder_path}")
    if not os.path.exists(REF_AUDIO_PATH):
        print(f"에러: 레퍼런스 오디오 파일을 찾을 수 없습니다: {REF_AUDIO_PATH}")
        return
    
    # 1. 레퍼런스 처리 (업로드만 진행, 트랜스크립션은 고정 텍스트 사용)
    print("[*] 레퍼런스 오디오 업로드 중...")
    ref_file_info = upload_file(REF_AUDIO_PATH)
    ref_text = REF_TEXT

    # 2. TTS 생성
    print("[*] Voice Clone 생성 중...")
    clone_data = [ref_file_info, ref_text, script_text, "Korean", False, "1.7B", 200, 0.0, -1]
    event_id = call_api("/generate_voice_clone", clone_data)
    result_data = get_result("/generate_voice_clone", event_id)
    
    audio_file_info = result_data[0]
    if not audio_file_info:
        print("에러: TTS 생성 실패")
        return

    # 3. 다운로드 및 배속 변환
    temp_wav = os.path.join(folder_path, "temp.wav")
    final_wav = os.path.join(folder_path, "output_1.2x.wav")
    
    remote_path = audio_file_info.get("path")
    audio_url = f"{BASE_URL}{API_PREFIX}/file={remote_path}"
    
    r = requests.get(audio_url, stream=True)
    if r.status_code == 200:
        with open(temp_wav, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        change_speed(temp_wav, final_wav)
        if os.path.exists(temp_wav): os.remove(temp_wav)
        print(f"[+] 성공: {final_wav}")
    else:
        print(f"에러: 다운로드 실패 ({r.status_code})")

if __name__ == "__main__":
    main()
