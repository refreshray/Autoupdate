import requests

# 1. URL ต้นทางของคุณ
M3U_URL = "https://github.com/cattv976/iptv/raw/refs/heads/main/cattv.m3u" # ตัวอย่างลิงก์ตามแท็บในภาพของคุณ

# 2. ชื่อช่องที่ต้องการ (แนะนำให้ใช้พิมพ์ใหญ่-เล็กให้ตรง หรือใส่แค่คำสำคัญสั้นๆ)
KEYWORDS = ["ALTV","CH5","T-SPorts7"]

def main():
    response = requests.get(M3U_URL)
    if response.status_code != 200:
        print("ไม่สามารถดาวน์โหลดไฟล์ต้นทางได้")
        return

    lines = response.text.splitlines()
    output_lines = ["#EXTM3U url-tvg=\"https://github.com/refreshray/epg-auto/raw/refs/heads/main/TV_epg.xml\"\n"]
    
    is_capturing = False # ตัวแปรเช็คว่าตอนนี้กำลังเก็บข้อมูลช่องที่เราต้องการอยู่ไหม

    for line in lines:
        # ตัดช่องว่างหัวท้ายออกเพื่อความแม่นยำ
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
                
        # ถ้าอยู่ในระหว่างการเก็บข้อมูลช่องที่เราเลือก
        elif is_capturing:
            output_lines.append(clean_line + "\n")
            # ถ้าเจอลิงก์สตรีมมิ่ง (มักขึ้นต้นด้วย http หรือ https) แปลว่าจบบล็อกของช่องนี้แล้ว
            if clean_line.startswith("http://") or clean_line.startswith("https://"):
                is_capturing = False # สั่งหยุดชั่วคราวเพื่อรอเจอ #EXTINF ช่องถัดไป

    # บันทึกเป็นไฟล์ใหม่
    with open("๊Update_playlist.m3u", "w", encoding="utf-8") as f:
        f.writelines(output_lines)
    print("กรองเพลย์ลิสต์ระบบขั้นสูงเสร็จเรียบร้อยแล้ว!")

if __name__ == "__main__":
    main()
