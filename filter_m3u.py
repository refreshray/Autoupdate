import requests

# 1. ใส่ URL ของไฟล์ M3U ต้นทางบน GitHub (ต้องเป็นลิงก์แบบ Raw เท่านั้น)
M3U_URL = "https://github.com/cattv976/iptv/raw/refs/heads/main/cattv.m3u"

# 2. ใส่ชื่อช่องที่คุณต้องการดึงมา (พิมพ์ให้ตรงหรือใกล้เคียงกับชื่อในไฟล์ต้นทาง)
KEYWORDS = ["Cinemax", "CH7", "HBO", "Mono29","HBOFamily"] 

def main():
    response = requests.get(M3U_URL)
    if response.status_code != 200:
        print("ไม่สามารถดาวน์โหลดไฟล์ต้นทางได้")
        return

    lines = response.text.splitlines()
    output_lines = ["#EXTM3U\n"] # บรรทัดเริ่มต้นของไฟล์ M3U
    
    # วนลูปอ่านทีละบรรทัด
    for i in range(len(lines)):
        if lines[i].startswith("#EXTINF"):
            # ตรวจสอบว่าบรรทัดนี้มีคำสำคัญที่เราต้องการไหม
            if any(keyword.lower() in lines[i].lower() for keyword in KEYWORDS):
                output_lines.append(lines[i] + "\n") # ใส่บรรทัด #EXTINF
                if i + 1 < len(lines):
                    output_lines.append(lines[i+1] + "\n") # ใส่บรรทัด URL ถัดมา

    # บันทึกเป็นไฟล์ใหม่
    with open("my_playlist.m3u", "w", encoding="utf-8") as f:
        f.writelines(output_lines)
    print("กรองเพลย์ลิสต์เสร็จเรียบร้อยแล้ว!")

if __name__ == "__main__":
    main()
