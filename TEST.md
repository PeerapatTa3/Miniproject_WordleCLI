# TEST.md — Miniproject_WordleCLI
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
  feedback = ["x"] * word_length
  secret_remaining = list(secret_word)
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
- **สถานะ:** ✅ แก้ไขแล้ว — เปลี่ยนเป็น two-pass algorithm claim ✓ ก่อน แล้วค่อยเช็ค "-" จากตัวอักษรที่เหลือ

---

## ✅ Test Cases (อัปเดตสำหรับ v1.0.0)

| # | Feature | Input / Steps | Expected Result | Actual (ก่อนแก้) | Actual (หลังแก้) | Status |
|---|---------|----------------|------------------|-------------------|-------------------|--------|
| TC-01 | เมนูหลัก | เลือก option 1-4 | แสดงเมนูถูกต้อง, เข้าฟังก์ชันตรงตามเลือก | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-02 | เมนูหลัก - invalid | พิมพ์ `9`, `abc`,ไม่พิมพ์แล้วกด Enter | แจ้ง "Invalid menu choice" ไม่ crash | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-03 | Play - ชนะเกม | เดาคำถูกภายใน 6 ครั้ง | แสดง feedback ทุกครั้ง, ขึ้นข้อความ 🎉 ชนะ | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-04 | Play - แพ้เกม | เดาผิดครบ 6 ครั้ง | แสดง "Out of attempts" พร้อมเฉลยคำลับ | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-05 | Play - input ผิดความยาว | พิมพ์ `AB` หรือ `TOOLONGWORD` | แจ้ง invalid, ไม่นับเป็น attempt | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-06 | Play - input ไม่ใช่ตัวอักษรหรือไม่พิมพ์แล้ว Enter | พิมพ์ `12345`, `AB!DE`,ปล่อยว่างแล้ว Enter | แจ้ง invalid, ไม่นับเป็น attempt | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-07 | Play - ตัวอักษรซ้ำในคำเดา | secret=`APPLE`, guess=`PAPAS` | feedback ต้องนับ P ตามจำนวนจริงในคำลับ (2 ตัว) | ❌ **Fail** (mark "-" เกิน) | ✅ Pass | ✅ Fixed |
| TC-08 | Play - เดาคำถูกทันที | guess = secret_word เลย | ชนะทันที, attempts = 1 | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-09 | View History - ว่าง | เลือก option 2 ก่อนเล่นเกม | แจ้ง "No guesses recorded yet" | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-10 | View History - มีข้อมูล | เล่นแล้วเลือก option 2 | แสดง original order + sorted order ถูกต้อง | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-11 | Remove Word - พบใน pool | เลือก option 3, พิมพ์คำที่มีจริง | ลบสำเร็จ, แสดงขนาด pool ใหม่ | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-12 | Remove Word - ไม่พบใน pool | พิมพ์คำที่ไม่มีใน pool | แจ้ง error, ไม่ crash, pool ไม่เปลี่ยน | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-13 | Remove Word - ลบจนหมด pool | ลบทีละคำจนกว่า pool ว่าง | แจ้ง auto-reset, pool กลับเป็น default 7 คำ | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-14 | Play - pool ว่างตอนเริ่มเกมใหม่ | ลบคำจนหมด แล้วเลือก option 1 | auto-reset pool ก่อนเริ่มเกม ไม่ crash | ตรงตามคาด | ตรงตามคาด | ✅ Pass |
| TC-15 | Exit | เลือก option 4 | แสดงข้อความลาก่อน, โปรแกรมจบ loop | ตรงตามคาด | ตรงตามคาด | ✅ Pass |


---

## ⚠️ Known Limitations (ไม่ใช่บั๊ก แต่ควร note ไว้)

1. **ไม่ตรวจสอบว่าคำเดาอยู่ในพจนานุกรม/word_pool**  ผู้เล่นเดาคำที่ไม่มีความหมาย (เช่น `AAAAA`) ก็ผ่าน validation ได้ เพราะระบบเช็คแค่ความยาว + isalpha
2. **`guess_history` สะสมข้ามเกม ไม่ reset ต่อรอบ**  

---

## สรุป

- บั๊กที่พบ: **1 รายการ (High severity)** — แก้ไขแล้ว
- Test cases ทั้งหมด: 16 เคส, ผ่าน 15, มี 1 known limitation ที่ยังไม่แก้
- ไฟล์ที่แก้ไข: `game.py` 


## ✅ Test Cases (อัปเดตสำหรับ v2.0.0)

| # | Feature | Input / Steps | Expected Result | Status |
|---|---------|----------------|------------------|--------|
| TC-01 | เมนูหลัก | เลือก option 1-5 | แสดงเมนูถูกต้อง, เข้าฟังก์ชันตรงตามที่เลือก | ✅ Pass |
| TC-02 | เมนูหลัก - invalid | พิมพ์ `9`, `abc`, ไม่พิมพ์แล้วกด Enter | แจ้ง "Invalid menu choice" ดักจับได้สมบูรณ์ ไม่ crash | ✅ Pass |
| TC-03 | Play - ชนะเกม | เดาคำถูกภายใน 6 ครั้ง | แสดง feedback ทุกครั้ง, ขึ้นข้อความ 🎉 ชนะ | ✅ Pass |
| TC-04 | Play - แพ้เกม | เดาผิดครบ 6 ครั้ง | แสดง "Out of attempts" พร้อมเฉลยคำลับ | ✅ Pass |
| TC-05 | Play - input ผิดความยาว | พิมพ์ `AB` หรือ `TOOLONGWORD` | แจ้ง invalid จากฟังก์ชัน `validate_input` ไม่นับเป็น attempt | ✅ Pass |
| TC-06 | Play - ไม่ใช่ตัวอักษร | พิมพ์ `12345` หรือ `AB!DE` | แจ้ง invalid จากฟังก์ชัน `validate_input` ไม่นับเป็น attempt | ✅ Pass |
| TC-07 | History - ข้อมูลว่าง | กดเมนู 2 ก่อนเล่น | แสดง "No guesses recorded yet." ไม่ crash | ✅ Pass |
| TC-08 | History - มีข้อมูล | เล่นจบ 1 เกมแล้วกดเมนู 2 | แสดงรายการคำเดาแยกตามรายเกม (Game 1, Game 2) ถูกต้อง | ✅ Pass |
| TC-09 | Stats - ข้อมูลว่าง | กดเมนู 3 ก่อนเล่น | แสดง "No stats available yet." หลีกเลี่ยง ZeroDivisionError | ✅ Pass |
| TC-10 | Stats - การคำนวณ | ชนะ 1 แพ้ 1 แล้วกดเมนู 3 | แสดง Win Rate, Streak คำนวณถูกต้อง, กราฟ █ แท่งถูกต้อง | ✅ Pass |
| TC-11 | How to Play | กดเมนู 4 | แสดงคู่มือการเล่นและคำอธิบายสัญลักษณ์ | ✅ Pass |
| TC-12 | Exit | เลือก option 5 | แสดงข้อความลาก่อน, โปรแกรมจบ loop | ✅ Pass |

---

## สรุป
- Test cases ทั้งหมด: 12 เคส (ปรับปรุงโครงสร้างตามเมนูใหม่ 5 เมนู)
- ตัด Test cases เกี่ยวกับการลบคำออก (Feature ถูกนำออกใน v2.0.0)
- บั๊กที่พบ: 0 รายการ (โค้ดรัดกุมขึ้นจากการแยกย่อยฟังก์ชัน)
