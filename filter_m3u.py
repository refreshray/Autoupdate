import requests

# 1. URL ต้นทางของคุณ
M3U_URL = "https://github.com/cattv976/iptv/raw/refs/heads/main/cattv.m3u"

# 2. ชื่อช่องที่ต้องการ (ระบบจะแปลงเป็นตัวพิมพ์เล็กให้อัตโนมัติอยู่แล้ว)
KEYWORDS = ["ALTV", "CH5", "T-Sports7"]

def main():
    try:
        response = requests.get(M3U_URL, timeout=10)
        if response.status_code != 200:
            print(f"ไม่สามารถดาวน์โหลดไฟล์ได้ (Status code: {response.status_code})")
            return
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")
        return

    lines = response.text.splitlines()
    output_lines = ['#EXTM3U url-tvg="https://github.com/refreshray/epg-auto/raw/refs/heads/main/TV_epg.xml"\n']
    
    is_capturing = False # ตัวแปรเช็คว่าตอนนี้กำลังเก็บข้อมูลช่องที่เราต้องการอยู่ไหม

    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            continue
            
        # ถ้าเจอขึ้นต้นด้วย #EXTINF ให้เช็คว่าใช่ช่องที่เราต้องการไหม
        if clean_line.startswith("#EXTINF:"):
            if any(keyword.lower() in clean_line.lower() for keyword in KEYWORDS):
                is_capturing = True
                output_lines.append(clean_line + "\n")
            else:
                is_capturing = False # ถ้าไม่ใช่ช่องที่เราต้องการ ก็หยุดเก็บข้อมูล
                
        # ถ้าอยู่ในระหว่างการเก็บข้อมูลช่องที่เราเลือก (รวมถึงบรรทัด #EXTVLCOPT หรือ URL)
        elif is_capturing:
            output_lines.append(clean_line + "\n")
            # ถ้าเจอลิงก์สตรีมมิ่ง แปลว่าจบบล็อกของช่องนี้แล้ว
            if clean_line.startswith("http://") or clean_line.startswith("https://"):
                is_capturing = False

    # บันทึกเป็นไฟล์ใหม่ (แก้ไขชื่อไฟล์ที่สะกดผิดแล้ว)
    output_filename = "Update_playlist.m3u"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.writelines(output_lines)
        
    print(f"กรองเพลย์ลิสต์เสร็จเรียบร้อย! บันทึกลงไฟล์ {output_filename} แล้ว (พบทั้งหมด {len(output_lines)} บรรทัด)")

if __name__ == "__main__":
    main()
