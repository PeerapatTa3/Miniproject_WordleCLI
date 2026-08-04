# TEST.md — Miniproject_WordleCLI

ผู้ทดสอบ (Debugger): นายพีรพล แก้วเจริญสันติสุข\
วันที่ทดสอบ: 4/8/2026\
ไฟล์ที่ทดสอบ: `game.py`\
วิธีทดสอบ: Manual testing รันโปรแกรมจริงผ่าน terminal, ป้อน input ตามเคสด้านล่าง

---

## 🐞 บั๊กที่พบ

### BUG-01: Feedback ไม่รองรับตัวอักษรซ้ำ (Duplicate Letter Handling)
- **ตำแหน่ง:** ส่วนคำนวณ `feedback` ใน option 1 (Play Wordle)
- **โค้ดเดิม:**
  ```python
  feedback = []
                for i in range(word_length):
                    if user_input[i] == secret_word[i]:
                        feedback.append("✓")
                    elif user_input[i] in secret_word:
                        feedback.append("-")
                    else:
                        feedback.append("x")
  ```
  - **โค้ดใหม่:**
  ```python
                for i in range(word_length):
                    if user_input[i] == secret_word[i]:
                        feedback[i] = "✓"
                        secret_remaining[i] = None

                for i in range(word_length):
                    if feedback[i] == "x" and user_input[i] in secret_remaining:
                        feedback[i] = "-"
                        secret_remaining[secret_remaining.index(user_input[i])] = None
  ```
- **ปัญหา:** ใช้ `in` ตรวจสอบว่ามีตัวอักษรอยู่ในคำลับหรือไม่ โดยไม่นับจำนวนตัวอักษรที่เหลือจริง ทำให้ตัวอักษรซ้ำถูก mark "-" เกินจำนวนจริงในคำลับ
- **Repro:** secret = `APPLE` (มี P 2 ตัว), guess = `PAPAS`
  - ผลลัพธ์เดิม (ผิด): P ทุกตัวในคำเดา ได้ "-" หมด ทั้งที่คำลับมี P แค่ 2 ตัว
  - ผลลัพธ์ที่ถูกต้อง: ตัว P ตัวที่ 3 ในคำเดา (ถ้ามี) ควรได้ "x" ไม่ใช่ "-"
- **Severity:** High — กระทบ core gameplay logic โดยตรง ทำให้ผู้เล่นได้ข้อมูลผิด
- **สถานะ:** ✅ แก้ไขแล้ว — เปลี่ยนเป็น two-pass algorithm (claim ✓ ก่อน แล้วค่อยเช็ค "-" จากตัวอักษรที่เหลือ) ดูใน `game.py` (คอมเมนต์ `BUG-01 FIX`)

---

## ✅ Test Cases

| # | Feature | Input / Steps | Expected Result | Actual (ก่อนแก้) | Actual (หลังแก้) | Status |
|---|---------|----------------|------------------|-------------------|-------------------|--------|
| TC-01 | เมนูหลัก | เลือก option 1-4 | แสดงเมนูถูกต้อง, เข้าฟังก์ชันตรงตามเลือก | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-02 | เมนูหลัก - invalid | พิมพ์ `9`, `abc` | แจ้ง "Invalid menu choice" ไม่ crash | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-03 | Play - ชนะเกม | เดาคำถูกภายใน 6 ครั้ง | แสดง feedback ทุกครั้ง, ขึ้นข้อความ 🎉 ชนะ | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-04 | Play - แพ้เกม | เดาผิดครบ 6 ครั้ง | แสดง "Out of attempts" พร้อมเฉลยคำลับ | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-05 | Play - input ผิดความยาว | พิมพ์ `AB` หรือ `TOOLONGWORD` | แจ้ง invalid, ไม่นับเป็น attempt | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-06 | Play - input ไม่ใช่ตัวอักษร | พิมพ์ `12345`, `AB!DE` | แจ้ง invalid, ไม่นับเป็น attempt | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-07 | Play - ตัวอักษรซ้ำในคำเดา | secret=`APPLE`, guess=`PAPAS` | feedback ต้องนับ P ตามจำนวนจริงในคำลับ (2 ตัว) | ❌ **Fail** (mark "-" เกิน) | ✅ Pass | ✅ Fixed |
| TC-08 | Play - เดาคำถูกทันที | guess = secret_word เลย | ชนะทันที, attempts = 1 | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-09 | View History - ว่าง | เลือก option 2 ก่อนเล่นเกม | แจ้ง "No guesses recorded yet" | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-10 | View History - มีข้อมูล | เล่นแล้วเลือก option 2 | แสดง original order + sorted order ถูกต้อง | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-11 | Remove Word - พบใน pool | เลือก option 3, พิมพ์คำที่มีจริง | ลบสำเร็จ, แสดงขนาด pool ใหม่ | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-12 | Remove Word - ไม่พบใน pool | พิมพ์คำที่ไม่มีใน pool | แจ้ง error, ไม่ crash, pool ไม่เปลี่ยน | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-13 | Remove Word - ลบจนหมด pool | ลบทีละคำจนกว่า pool ว่าง | แจ้ง auto-reset, pool กลับเป็น default 7 คำ | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-14 | Play - pool ว่างตอนเริ่มเกมใหม่ | ลบคำจนหมด แล้วเลือก option 1 | auto-reset pool ก่อนเริ่มเกม ไม่ crash | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-15 | Exit | เลือก option 4 | แสดงข้อความลาก่อน, โปรแกรมจบ loop | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-16 | Robustness - EOF / empty input | กด Enter เปล่า, หรือ pipe ปิด stdin | ⚠️ ยังไม่ได้ handle → อาจ crash ด้วย `EOFError` | - | - | 🔶 Known limitation (ดูด้านล่าง) |

---

## ⚠️ Known Limitations (ไม่ใช่บั๊ก แต่ควร note ไว้)

1. **ไม่ตรวจสอบว่าคำเดาอยู่ในพจนานุกรม/word_pool**  ผู้เล่นเดาคำที่ไม่มีความหมาย (เช่น `AAAAA`) ก็ผ่าน validation ได้ เพราะระบบเช็คแค่ความยาว + isalpha
2. **ไม่ handle `EOFError`**  ถ้า stdin ปิดกะทันหัน เช่นรันผ่าน automated pipe โปรแกรมจะ crash แทนที่จะ exit อย่างสุภาพ
3. **`guess_history` สะสมข้ามเกม ไม่ reset ต่อรอบ**  

---

## สรุป

- บั๊กที่พบ: **1 รายการ (High severity)** — แก้ไขแล้ว
- Test cases ทั้งหมด: 16 เคส, ผ่าน 15, มี 1 known limitation ที่ยังไม่แก้
- ไฟล์ที่แก้ไข: `game.py` 
