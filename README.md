<div align="center">

# 📊 InvestAnalyst

**ระบบกรอบการวิเคราะห์การลงทุนและประเมินมูลค่าหุ้นสหรัฐฯ (Investment Analysis Skills & Knowledge Hub)**

</div>

---

## 🎯 โครงสร้างโปรเจกต์ (Project Structure)

โปรเจกต์นี้ได้รับการจัดระเบียบให้มีเฉพาะส่วนสำคัญ 3 ด้านหลัก:

```text
InvestAnalyst/
├── .agents/
│   └── skills/           # 🧠 คลัง AI Skills สำหรับการวิเคราะห์หุ้น (27 ทักษะ)
├── prompts/              # 📝 Prompt Frameworks สำหรับการวิเคราะห์
├── data/                 # 📚 ข้อมูลความรู้และงบการเงินตัวอย่าง (10-K Reports)
├── site/                 # 🌐 ระบบเว็บไซต์ความรู้และคู่มือการเรียนรู้
│   ├── content/          # เนื้อหาบทเรียนความรู้การลงทุน (รวมฉบับภาษาไทย -th)
│   ├── learning-th.html  # หน้าเว็บไซต์ศูนย์การเรียนรู้ภาษาไทย
│   └── build/            # สไตล์และสคริปต์แสดงผลเว็บไซต์
├── scripts/
│   └── generate_th_html.py # สคริปต์คอมไพล์เอกสารภาษาไทยเป็นเว็บ HTML
├── AGENTS.md             # ⚙️ กฎและค่ากำหนดภาษาของ Agent (ตอบภาษาไทย)
└── README.md             # 📖 เอกสารแนะนำโปรเจกต์
```

---

## 🚀 1. คลังทักษะการวิเคราะห์ (Analysis Skills & Prompts)

มีทักษะการวิเคราะห์ครอบคลุม 27 ด้าน เช่น:

| หมวดหมู่ | ตัวอย่าง Skills (`.agents/skills/` & `prompts/`) | สิ่งที่ได้จากการวิเคราะห์ |
| :--- | :--- | :--- |
| **Core Analysis** | `stock-eval`, `fundamental-analysis`, `technical-analysis`, `dcf-valuation` | วิเคราะห์งบการเงิน, กราฟเทคนิค, ประเมินมูลค่ากระแสเงินสดคิดลด (DCF) |
| **Filing Analysis** | `10k-digest`, `financial-report-analyst`, `earnings-call-analysis` | สรุปรายงานประจำปี 10-K, วิเคราะห์ Oppday/Earnings Call |
| **Market & Money** | `institutional-ownership`, `insider-trading`, `short-interest`, `dividend-analysis` | ติดตาม Smart Money, การซื้อขายของผู้บริหาร, อัตรา Short Squeeze |
| **Advanced & Strategy** | `competitor-analysis`, `industry-map`, `position-ladder`, `bear-case` | แผนที่ Value Chain อุตสาหกรรม, กลยุทธ์วางโซนราคา (Ladder), มุมมอง Bear Case |

---

## 📚 2. ข้อมูลความรู้การลงทุน (Data & Learning Content)

- **`data/`**: เอกสารรายงานการเงินจริง (เช่น `NVDA_2026_10-K.pdf`, `AMD_2026_10-K.pdf`) สำหรับใช้ในการทดสอบและดึงข้อมูลเชิงลึก
- **`site/content/`**: บทเรียนและคลังความรู้การลงทุน 8 บทหลัก และพจนานุกรมคำศัพท์ (มีทั้งฉบับภาษาไทยและอังกฤษ)

---

## 🌐 3. เว็บไซต์การเรียนรู้ (Web & Learning Hub)

- สามารถเปิดไฟล์ [`site/learning-th.html`](site/learning-th.html) บน Browser ได้ทันที เพื่ออ่านคู่มือและบทเรียนการวิเคราะห์ทั้งหมดในภาษาไทย
- หากมีการแก้ไขเนื้อหาใน `site/content/*-th.md` สามารถรันคำสั่งอัปเดตหน้าเว็บได้ด้วย:
  ```bash
  python scripts/generate_th_html.py
  ```

---

## ⚙️ การใช้งานกับ AI Agent

โปรเจกต์นี้ตั้งค่าคำสั่งใน [`AGENTS.md`](AGENTS.md) ให้ตอบและสรุปผลการวิเคราะห์เป็น **ภาษาไทย** โดยอัตโนมัติ พร้อมอ้างอิงศัพท์การเงินสากลเพื่อความแม่นยำ

---

## ⚖️ ข้อจำกัดความรับผิดชอบ (Disclaimer)

*ข้อมูลและกรอบการวิเคราะห์ทั้งหมดในโปรเจกต์นี้มีไว้เพื่อวัตถุประสงค์ในการศึกษาและการวิจัยเท่านั้น ไม่ถือเป็นคำแนะนำทางการเงินหรือการชักชวนให้ซื้อขายหลักทรัพย์ใดๆ*

---

## 📄 License

MIT License
