#!/usr/bin/env python3
"""
crop_asset_sheet.py
- 종합 에셋 시트(asset_sheet.jpg, 16:9)에서 4~8개의 사진 패널들을 자동 감지하고,
  각 패널을 찌그러짐 없이 완벽한 9:16 쇼츠 규격(1080x1920)으로 스마트 크롭 및 저장합니다.
- 1행(1x3) 및 2행 다중 그리드(2x2, 2x3, 2x4 등 4~8컷)를 완벽 지원합니다.
"""

import sys
import os
import cv2
import numpy as np
from PIL import Image

TARGET_WIDTH = 1080
TARGET_HEIGHT = 1920

def process_single_sheet(sheet_path, assets_dir, prefix, start_idx=1):
    pil_img = Image.open(sheet_path)
    w, h = pil_img.size
    src = cv2.imread(sheet_path)
    sorted_boxes = []

    if src is not None:
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        min_area = (w * h) * 0.05

        valid_boxes = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < min_area:
                continue
            x, y, bw, bh = cv2.boundingRect(cnt)
            aspect_ratio = bh / float(bw)
            if 0.8 <= aspect_ratio <= 3.5:
                valid_boxes.append((x, y, bw, bh))

        if len(valid_boxes) >= 2:
            avg_h = sum(b[3] for b in valid_boxes) / len(valid_boxes)
            row_threshold = avg_h * 0.5
            valid_boxes.sort(key=lambda b: b[1])

            rows = []
            current_row = [valid_boxes[0]]
            for b in valid_boxes[1:]:
                if abs(b[1] - current_row[0][1]) < row_threshold:
                    current_row.append(b)
                else:
                    current_row.sort(key=lambda b: b[0])
                    rows.append(current_row)
                    current_row = [b]
            current_row.sort(key=lambda b: b[0])
            rows.append(current_row)
            sorted_boxes = [box for row in rows for box in row]

    # 컨투어 검출 실패 시 또는 1x3 기본 3분할 폴백
    if len(sorted_boxes) < 2:
        print("  [*] 1x3 단일 행 스마트 균등 3분할 모드로 처리합니다.")
        num_cuts = 3
        sorted_boxes = []
        for i in range(num_cuts):
            x1 = int(i * (w / float(num_cuts)))
            x2 = int((i + 1) * (w / float(num_cuts)))
            sorted_boxes.append((x1, 0, x2 - x1, h))

    saved_count = 0
    current_cut_idx = start_idx

    for i, (bx, by, bw, bh) in enumerate(sorted_boxes):
        crop_x1 = max(0, bx + 1)
        crop_y1 = max(0, by + 1)
        crop_x2 = min(w, bx + bw - 1)
        crop_y2 = min(h, by + bh - 1)

        raw_panel = pil_img.crop((crop_x1, crop_y1, crop_x2, crop_y2))
        np_panel = np.array(raw_panel)

        # 빈 슬롯 검출: 완전 검정색(mean < 20)이거나 단색 배경(std < 8)인 경우 스킵
        if np_panel.size > 0:
            mean_val = np.mean(np_panel)
            std_val = np.std(np_panel)
            if mean_val < 20 or std_val < 8:
                print(f"  [-] 빈 슬롯(Black/Blank panel) 감지됨: {i+1}번째 패널 스킵")
                continue

        pw, ph = raw_panel.size
        current_ar = ph / float(pw)
        target_ar = 16.0 / 9.0

        if current_ar > target_ar:
            new_h = int(pw * target_ar)
            top = max(0, (ph - new_h) // 2)
            panel_9_16 = raw_panel.crop((0, top, pw, top + new_h))
        else:
            new_w = int(ph / target_ar)
            left = max(0, (pw - new_w) // 2)
            panel_9_16 = raw_panel.crop((left, 0, left + new_w, ph))

        final_9_16 = panel_9_16.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
        out_filename = f"{prefix}{current_cut_idx}_9_16.jpg"
        out_path = os.path.join(assets_dir, out_filename)
        final_9_16.save(out_path, quality=95)
        print(f"  [+] 저장 완료: {out_filename} (1080x1920 9:16)")
        current_cut_idx += 1
        saved_count += 1

    return saved_count

def crop_asset_sheet(folder_path, is_faction=False):
    assets_dir = os.path.join(folder_path, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    prefix = "scene" if is_faction else "cut"

    # 다중 시트 탐색: asset_sheet_1.jpg, asset_sheet_2.jpg ... 또는 단일 asset_sheet.jpg
    import glob
    sheet_files = sorted(glob.glob(os.path.join(folder_path, "asset_sheet_*.jpg")))
    single_sheet = os.path.join(folder_path, "asset_sheet.jpg")
    
    if not sheet_files and os.path.exists(single_sheet):
        sheet_files = [single_sheet]

    if not sheet_files:
        print(f"[!] 에러: {folder_path} 내에 asset_sheet.jpg 또는 asset_sheet_*.jpg 파일이 존재하지 않습니다.")
        return False

    total_saved = 0
    next_idx = 1
    for sheet_path in sheet_files:
        print(f"[*] 에셋 시트 처리 중: {os.path.basename(sheet_path)}")
        saved = process_single_sheet(sheet_path, assets_dir, prefix, start_idx=next_idx)
        next_idx += saved
        total_saved += saved

    print(f"[✓] 에셋 시트 분할 및 9:16 보정 완료! 총 {total_saved}개 에셋이 {assets_dir}에 저장되었습니다.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python3 crop_asset_sheet.py <outputs/프로젝트폴더>")
        sys.exit(1)
    
    target_folder = sys.argv[1]
    crop_asset_sheet(target_folder)
