# Agent Instructions & Project Preferences

## Language Preference (การตั้งค่าภาษา)
- **Default Language (ภาษาหลัก):** ตอบคำถาม อธิบาย และสรุปผลการวิเคราะห์ทั้งหมดเป็น **ภาษาไทย** เป็นหลัก
- **Technical & Financial Terms:** สามารถใช้คำศัพท์เฉพาะทางด้านการเงิน การลงทุน บัญชี หรือชื่อย่อของตัวชี้วัดทางการเงิน (เช่น P/E, P/B, ROIC, WACC, DCF, Gross Margin, Free Cash Flow, Ticker/ISIN) เป็นภาษาอังกฤษได้ตามความเหมาะสมเพื่อความถูกต้องและชัดเจน
- **Code & Syntax:** รักษารูปแบบ Format, สัญลักษณ์ และโค้ดตามมาตรฐานของแต่ละ Skill / Framework

## Analysis Guidelines
- ปฏิบัติตามคำแนะนำและกรอบการวิเคราะห์ใน prompts/ และ .agents/skills/ อย่างครบถ้วน
- สรุปภาพรวมและกลยุทธ์การลงทุนให้เข้าใจง่าย ชัดเจน และนำไปใช้งานได้จริง

## Mermaid Diagram Rules (กฎการใช้ Mermaid Diagram)
- **ห้ามใช้ `mindmap`, `timeline` หรือ diagram types ที่ไม่รองรับเด็ดขาด** (ป้องกันปัญหา Render Error)
- **Supported Types ที่อนุญาตให้ใช้:** `flowchart TD/LR`, `graph TD/LR`, `sequenceDiagram`, `classDiagram`, `stateDiagram-v2`, `erDiagram`, `xychart-beta` เท่านั้น
- เมื่อต้องการสร้างแผนผังความคิด (Mindmap) ให้ใช้ `flowchart LR` หรือ `graph TD` แทนเสมอ

## Git Workflow & Quality Assurance Rules
1. **Commit after every file modification**: ทุกครั้งที่มีการแก้ไข เพิ่ม หรือเปลี่ยนแปลงไฟล์ในโปรเจกต์ ต้องตรวจสอบ bug / syntax ให้เรียบร้อย แล้วทำการ `git commit` ทันที
2. **Commit Message Reporting**: ต้องแจ้งผู้ใช้ทุกครั้งว่า commit ไปว่าอะไร (Commit Message)
3. **NEVER PUSH**: **ห้าม `git push` โดยเด็ดขาด** จนกว่าผู้ใช้จะสั่งเท่านั้น

## Safety Rules (กฎความปลอดภัย)
- **ห้ามลบไฟล์โดยไม่ถามเด็ดขาด (Never delete files without permission):** ห้ามลบไฟล์หรือไดเรกทอรีใด ๆ ในโปรเจกต์โดยไม่ได้รับความยินยอมหรือการยืนยันจากผู้ใช้ก่อนเด็ดขาด

