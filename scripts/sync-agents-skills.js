const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, '..', 'plugins', 'us-stock-analysis', 'skills');
const destBase = path.join(__dirname, '..', '.agents', 'skills');

if (!fs.existsSync(srcDir)) {
  console.error("Source dir not found:", srcDir);
  process.exit(1);
}

const entries = fs.readdirSync(srcDir, { withFileTypes: true });

for (const entry of entries) {
  if (!entry.isDirectory()) continue;
  const skillName = entry.name;
  const srcSkillFile = path.join(srcDir, skillName, 'SKILL.md');
  const targetDir = path.join(destBase, skillName);
  const targetSkillFile = path.join(targetDir, 'SKILL.md');

  if (fs.existsSync(srcSkillFile)) {
    if (!fs.existsSync(targetDir)) {
      fs.mkdirSync(targetDir, { recursive: true });
    }
    let content = fs.readFileSync(srcSkillFile, 'utf8');
    if (!/^name:\s*/m.test(content)) {
      content = content.replace(/^---\r?\n/, `---\nname: ${skillName}\n`);
    }
    fs.writeFileSync(targetSkillFile, content, 'utf8');
    console.log(`Synced: ${skillName}`);
  }
}
