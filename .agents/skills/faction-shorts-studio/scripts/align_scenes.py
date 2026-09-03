import os
import json
import sys
import glob
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

FPS = 30

# 팩션 썰쇼츠 전용: 1.5배속 wav 파일명
WAV_FILENAME = "output_1.5x.wav"

def get_stt_data(file_path):
    with open(file_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )
    return response.segments

def refine_text_llm(segments, script_text):
    stt_texts = [f"[{i}] {seg.text}" for i, seg in enumerate(segments)]
    stt_combined = "\n".join(stt_texts)
    
    prompt = """
    원본 대본을 참고하여 STT 결과를 자막용으로 교정하고, 모바일 쇼츠 영상에 어울리도록 자막의 호흡을 아주 짧고 직관적으로 쪼개어 구성하세요.
    
    [교정 및 분할 가이드라인]
    1. **자막 길이 제한**: 한 화면에 표시될 각 자막 텍스트는 2~4단어 내외(어절 수 2~4개, 15자 이내)로 아주 짧아야 합니다. (예: "데이터를 많이 넣으려고", "AI 소프트웨어를", "혁신이 일어날 거라고")
    2. **의미 단위 분할**: 조사나 어미 등이 중간에 뜬금없이 끊기지 않도록 주어, 목적어, 서술어 등 한국어의 의미적 호흡(의미 단위)을 철저히 고려하여 자연스럽게 문장을 쪼개세요.
       - 나쁜 예: "전 세계" / "기업 10곳 중" / "9곳이 AI를" / "쓰고 있습니다." (의미 호흡 어색)
       - 좋은 예: "전 세계 기업 중" / "10곳 중 9곳이" / "AI를 쓰고 있습니다."
    3. **정밀한 인덱스 매핑**: 각 쪼개진 자막 텍스트가 원래 STT 결과의 어떤 segment(들)에 해당하는지 인덱스 번호 배열(indices)을 정확히 매핑하여 반환하세요. 보통 한 자막당 매핑되는 인덱스는 1~2개 내외여야 합니다.
    4. 숫자 및 단위 교정 (예: 칠십 퍼센트 -> 70%)
    5. 고유명사 교정 (예: 에이아이 -> AI, 쥐스택 -> G-Stack, 슈퍼파워스 -> Superpowers)
    6. 반환 형식은 반드시 아래 예시와 같은 JSON 배열 형식이어야 합니다. 마크다운 백틱(```json)을 제외한 다른 설명 텍스트는 일체 출력하지 마세요.
    
    [반환 형식 예시]
    [
      {
        "text": "전 세계 기업 중",
        "indices": [0]
      },
      {
        "text": "10곳 중 9곳이",
        "indices": [1]
      },
      {
        "text": "AI를 쓰고 있습니다.",
        "indices": [2]
      }
    ]
    
    [원본 대본]
    {script_text}
    
    [STT 결과]
    {stt_combined}
    """
    prompt = prompt.replace("{script_text}", script_text).replace("{stt_combined}", stt_combined)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    content = response.choices[0].message.content.strip()
    if content.startswith("```json"): content = content[7:-3].strip()
    elif content.startswith("```"): content = content[3:-3].strip()
    return json.loads(content)

def main():
    if len(sys.argv) < 2: return
    folder = sys.argv[1]
    wav_path = os.path.join(folder, WAV_FILENAME)
    
    md_files = glob.glob(os.path.join(folder, "*.md"))
    if not md_files:
        print(f"에러: {folder} 내에 MD 대본 파일이 없습니다.")
        return
    
    # script.md를 우선 찾고, 없으면 아무 .md 파일
    script_path = os.path.join(folder, "script.md")
    if not os.path.exists(script_path):
        script_path = md_files[0]
    
    with open(script_path, 'r', encoding='utf-8') as f: 
        script_text = f.read()

    print(f"[*] STT 시작: {wav_path}")
    segments = get_stt_data(wav_path)
    
    # RAW 저장
    raw_path = os.path.join(folder, "raw_stt.json")
    with open(raw_path, 'w', encoding='utf-8') as f:
        json.dump([{"text": s.text, "start": s.start, "end": s.end} for s in segments], f, ensure_ascii=False, indent=2)

    print(f"[*] 하이브리드 교정 및 병합 중...")
    try:
        refined_blocks = refine_text_llm(segments, script_text)
        if not isinstance(refined_blocks, list) or not all(isinstance(b, dict) and "text" in b and "indices" in b for b in refined_blocks):
            raise ValueError("Invalid LLM response format")
    except Exception as e:
        print(f"[!] LLM 교정/병합 실패. 기본 STT 결과를 사용합니다. 에러: {e}")
        refined_blocks = [{"text": seg.text, "indices": [i]} for i, seg in enumerate(segments)]
    
    print(f"[*] 씬 그룹화 중 (쇼츠 자막 단위 씬 분할)...")
    
    # 1. 각 segment를 참조하는 블록들의 인덱스 매핑 생성
    seg_to_blocks = {}
    for block_idx, block in enumerate(refined_blocks):
        for seg_idx in block["indices"]:
            if 0 <= seg_idx < len(segments):
                if seg_idx not in seg_to_blocks:
                    seg_to_blocks[seg_idx] = []
                seg_to_blocks[seg_idx].append(block_idx)

    # 2. 각 segment를 텍스트 길이에 따라 시간 분할
    block_seg_times = {}
    for seg_idx, block_indices in seg_to_blocks.items():
        seg = segments[seg_idx]
        total_duration = seg.end - seg.start
        
        weights = []
        for b_idx in block_indices:
            text_len = max(1, len(refined_blocks[b_idx]["text"].replace(" ", "")))
            weights.append(text_len)
            
        total_weight = sum(weights)
        
        current_offset = 0.0
        for i, b_idx in enumerate(block_indices):
            weight = weights[i]
            duration = total_duration * (weight / total_weight)
            
            sub_start = seg.start + current_offset
            sub_end = sub_start + duration
            current_offset += duration
            
            if b_idx not in block_seg_times:
                block_seg_times[b_idx] = {}
            block_seg_times[b_idx][seg_idx] = (sub_start, sub_end)

    # 3. 각 블록의 최종 start/end 계산
    scenes = []
    scene_id = 1
    
    for block_idx, block in enumerate(refined_blocks):
        text = block["text"]
        indices = block["indices"]
        
        valid_indices = [idx for idx in indices if 0 <= idx < len(segments)]
        if not valid_indices:
            continue
            
        first_seg = valid_indices[0]
        start = block_seg_times[block_idx][first_seg][0]
        
        last_seg = valid_indices[-1]
        end = block_seg_times[block_idx][last_seg][1]
        
        start = round(start, 2)
        end = round(end, 2)
        
        scenes.append(create_scene(scene_id, [{"text": text, "start": start, "end": end}]))
        scene_id += 1
    
    out_path = os.path.join(folder, "scene_data.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(scenes, f, ensure_ascii=False, indent=2)
    print(f"[+] 성공: {out_path}")

def create_scene(scene_id, blocks):
    start, end = blocks[0]["start"], blocks[-1]["end"]
    return {
        "scene_id": scene_id,
        "start": start, "end": end,
        "duration_frames": int((end - start) * FPS),
        "text_blocks": blocks
    }

if __name__ == "__main__":
    main()
