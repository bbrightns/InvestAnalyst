import os
import json
import re

files = {
    'commands': ('⚡ คู่มือแนะนำการใช้งานทุกคำสั่ง (27 Skills)', 'site/content/COMMANDS-GUIDE-th.md'),
    'learning': ('ภาพรวมบทเรียน (Learning Hub)', 'site/content/LEARNING-th.md'),
    'foundations': ('บทที่ 1 · พื้นฐานการลงทุน (Foundations)', 'site/content/LEARNING-FOUNDATIONS-th.md'),
    'statements': ('บทที่ 2 · การอ่านงบการเงิน (Financial Statements)', 'site/content/LEARNING-STATEMENTS-th.md'),
    'quality': ('บทที่ 3 · คุณภาพธุรกิจและ Moat (Business Quality)', 'site/content/LEARNING-QUALITY-th.md'),
    'valuation': ('บทที่ 4 · การประเมินมูลค่าหุ้น (Valuation Essentials)', 'site/content/LEARNING-VALUATION-th.md'),
    'market': ('บทที่ 5 · การอ่านสัญญาณตลาด (Reading the Market)', 'site/content/LEARNING-MARKET-th.md'),
    'portfolio': ('บทที่ 6 · การจัดพอร์ตและความเสี่ยง (Portfolio & Risk)', 'site/content/LEARNING-PORTFOLIO-th.md'),
    'playbook': ('บทที่ 7 · เพลย์บุ๊กมืออาชีพ (The Pro Playbook)', 'site/content/LEARNING-PLAYBOOK-th.md'),
    'case-amd': ('บทที่ 8 · กรณีศึกษาหุ้น AMD (Case Study: AMD)', 'site/content/LEARNING-CASE-AMD-th.md'),
    'concepts': ('แนวคิดหลัก & แบบจำลองความคิด (Concepts)', 'site/content/CONCEPTS-th.md'),
    'glossary': ('พจนานุกรมคำศัพท์การเงิน A-Z (Glossary)', 'site/content/GLOSSARY-th.md')
}

def escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def make_slug(text):
    # Strip HTML tags
    clean = re.sub(r'<[^>]+>', '', text)
    # Match english words/chars first
    slug = clean.strip().lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    return slug.strip('-')

def md_to_html(md_text, current_page_key):
    lines = md_text.split('\n')
    html_lines = []
    in_table = False
    table_lines = []
    in_code = False
    code_lines = []
    code_lang = ''
    in_ul = False
    in_ol = False
    in_quote = False
    quote_lines = []

    def flush_table():
        nonlocal in_table, table_lines
        if not table_lines:
            in_table = False
            return
        
        res = ['<div class="table-responsive"><table>']
        header_done = False
        for r_idx, r in enumerate(table_lines):
            r = r.strip()
            if not r or r.startswith('|---') or r.startswith('| ---'):
                header_done = True
                continue
            cells = [c.strip() for c in r.strip('|').split('|')]
            if not header_done and r_idx == 0:
                res.append('<thead><tr>')
                for c in cells:
                    res.append(f'<th>{parse_inline(c)}</th>')
                res.append('</tr></thead><tbody>')
            else:
                res.append('<tr>')
                for c in cells:
                    res.append(f'<td>{parse_inline(c)}</td>')
                res.append('</tr>')
        if header_done:
            res.append('</tbody>')
        res.append('</table></div>')
        html_lines.append('\n'.join(res))
        table_lines = []
        in_table = False

    def flush_quote():
        nonlocal in_quote, quote_lines
        if not quote_lines:
            in_quote = False
            return
        content = '<br>'.join([parse_inline(l) for l in quote_lines])
        html_lines.append(f'<blockquote><p>{content}</p></blockquote>')
        quote_lines = []
        in_quote = False

    def parse_inline(text):
        # Code inline
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        # Bold
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
        # Italic
        text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
        # Links
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: f'<a href="{clean_href(m.group(2))}">{m.group(1)}</a>', text)
        return text

    def clean_href(href):
        # glossary.html#piotroski-f-score -> #glossary:piotroski-f-score
        for target_key in ['foundations', 'statements', 'quality', 'valuation', 'market', 'portfolio', 'playbook', 'case-amd', 'learning', 'concepts', 'glossary', 'commands']:
            pattern_file = f'{target_key}.html' if target_key not in ['foundations', 'statements', 'quality', 'valuation', 'market', 'portfolio', 'playbook', 'case-amd'] else f'learning-{target_key}.html'
            if pattern_file in href:
                if '#' in href:
                    part_anchor = href.split('#')[1]
                    return f'#{target_key}:{part_anchor}'
                return f'#{target_key}'

        if href.startswith('#'):
            anchor = href[1:]
            return f'#{current_page_key}:{anchor}'
            
        return href

    for line in lines:
        stripped = line.strip()

        # Code block
        if stripped.startswith('```'):
            if in_code:
                in_code = False
                escaped = escape_html('\n'.join(code_lines))
                html_lines.append(f'<pre><code>{escaped}</code></pre>')
                code_lines = []
            else:
                if in_table: flush_table()
                if in_quote: flush_quote()
                if in_ul: html_lines.append('</ul>'); in_ul = False
                if in_ol: html_lines.append('</ol>'); in_ol = False
                in_code = True
                code_lang = stripped[3:].strip()
            continue

        if in_code:
            code_lines.append(line)
            continue

        # Blockquote
        if stripped.startswith('>'):
            if in_table: flush_table()
            if in_ul: html_lines.append('</ul>'); in_ul = False
            if in_ol: html_lines.append('</ol>'); in_ol = False
            in_quote = True
            quote_lines.append(stripped.lstrip('> ').strip())
            continue
        elif in_quote and stripped != '':
            quote_lines.append(stripped)
            continue
        elif in_quote and stripped == '':
            flush_quote()
            continue

        # Table
        if stripped.startswith('|') and stripped.endswith('|'):
            if in_quote: flush_quote()
            if in_ul: html_lines.append('</ul>'); in_ul = False
            if in_ol: html_lines.append('</ol>'); in_ol = False
            in_table = True
            table_lines.append(stripped)
            continue
        elif in_table:
            flush_table()

        # Unordered List
        if stripped.startswith('- ') or stripped.startswith('* '):
            if in_table: flush_table()
            if in_quote: flush_quote()
            if in_ol: html_lines.append('</ol>'); in_ol = False
            if not in_ul:
                html_lines.append('<ul>')
                in_ul = True
            item_text = stripped[2:].strip()
            html_lines.append(f'<li>{parse_inline(item_text)}</li>')
            continue
        elif in_ul and not (stripped.startswith('- ') or stripped.startswith('* ')):
            if stripped == '':
                html_lines.append('</ul>')
                in_ul = False

        # Ordered list
        m_ol = re.match(r'^(\d+)\.\s+(.*)$', stripped)
        if m_ol:
            if in_table: flush_table()
            if in_quote: flush_quote()
            if in_ul: html_lines.append('</ul>'); in_ul = False
            if not in_ol:
                html_lines.append('<ol>')
                in_ol = True
            html_lines.append(f'<li>{parse_inline(m_ol.group(2))}</li>')
            continue
        elif in_ol and not m_ol:
            if stripped == '':
                html_lines.append('</ol>')
                in_ol = False

        if stripped == '':
            continue

        # Headings with explicit id and anchor
        if stripped.startswith('#### '):
            h_text = stripped[5:]
            slug = make_slug(h_text)
            html_lines.append(f'<h4 id="{slug}">{parse_inline(h_text)}</h4>')
        elif stripped.startswith('### '):
            h_text = stripped[4:]
            # If format like "### Altman Z-Score" -> slug "altman-z-score"
            # If format like "### 1. `stock-eval`" -> slug "stock-eval"
            m_skill = re.search(r'`([^`]+)`', h_text)
            slug = m_skill.group(1) if m_skill else make_slug(h_text)
            html_lines.append(f'<h3 id="{slug}">{parse_inline(h_text)}</h3>')
        elif stripped.startswith('## '):
            h_text = stripped[3:]
            # e.g. "## A" -> id "a", "## 1. Core..." -> id "1-core-stock-analysis"
            slug = make_slug(h_text)
            html_lines.append(f'<h2 id="{slug}">{parse_inline(h_text)}</h2>')
        elif stripped.startswith('# '):
            h_text = stripped[2:]
            slug = make_slug(h_text)
            html_lines.append(f'<h1 id="{slug}">{parse_inline(h_text)}</h1>')
        elif stripped.startswith('---'):
            html_lines.append('<hr>')
        else:
            html_lines.append(f'<p>{parse_inline(stripped)}</p>')

    if in_code:
        escaped = escape_html('\n'.join(code_lines))
        html_lines.append(f'<pre><code>{escaped}</code></pre>')
    if in_table: flush_table()
    if in_quote: flush_quote()
    if in_ul: html_lines.append('</ul>')
    if in_ol: html_lines.append('</ol>')

    return '\n'.join(html_lines)

rendered_articles = {}
for key, (title, path) in files.items():
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            md_content = f.read()
            rendered_articles[key] = {
                'title': title,
                'html': md_to_html(md_content, key)
            }

articles_json = json.dumps(rendered_articles, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>InvestSkill — คอร์สเรียนวิเคราะห์หุ้นสหรัฐฯ ฉบับภาษาไทย</title>
    <!-- Google Fonts: Sarabun & Inter -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sarabun:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0f141c;
            --bg-secondary: #161f2e;
            --bg-tertiary: #1f2c40;
            --border-color: #27364b;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --accent-blue: #38bdf8;
            --accent-green: #4ade80;
            --accent-yellow: #facc15;
            --accent-red: #f87171;
            --accent-purple: #c084fc;
            --sidebar-width: 335px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Sarabun', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.8;
            font-size: 16.5px;
            overflow-x: hidden;
            display: flex;
            height: 100vh;
        }

        /* Sidebar */
        #sidebar {
            width: var(--sidebar-width);
            min-width: var(--sidebar-width);
            background-color: var(--bg-secondary);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            height: 100vh;
            overflow-y: auto;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .brand {
            padding: 24px 20px;
            border-bottom: 1px solid var(--border-color);
            background: linear-gradient(180deg, rgba(56, 189, 248, 0.08) 0%, transparent 100%);
        }

        .brand-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .brand-badge {
            background: rgba(74, 222, 128, 0.18);
            color: var(--accent-green);
            font-size: 0.75rem;
            padding: 2px 8px;
            border-radius: 12px;
            border: 1px solid rgba(74, 222, 128, 0.4);
            font-weight: 600;
        }

        .brand-subtitle {
            font-size: 0.86rem;
            color: var(--text-secondary);
            margin-top: 6px;
            line-height: 1.4;
        }

        .search-box {
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-color);
        }

        .search-input {
            width: 100%;
            padding: 9px 14px;
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-primary);
            font-family: inherit;
            font-size: 0.92rem;
            outline: none;
            transition: all 0.2s;
        }

        .search-input:focus {
            border-color: var(--accent-blue);
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2);
        }

        .nav-section {
            padding: 16px 12px 30px;
        }

        .nav-heading {
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--text-muted);
            padding: 12px 12px 6px;
        }

        .nav-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 11px 14px;
            border-radius: 8px;
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.94rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.15s ease;
            margin-bottom: 3px;
            border: 1px solid transparent;
            line-height: 1.4;
        }

        .nav-item:hover {
            background-color: var(--bg-tertiary);
            color: var(--text-primary);
        }

        .nav-item.active {
            background-color: rgba(56, 189, 248, 0.12);
            color: var(--accent-blue);
            border-color: rgba(56, 189, 248, 0.3);
            font-weight: 600;
        }

        .nav-item.highlight {
            border: 1px dashed rgba(250, 204, 21, 0.4);
            background: rgba(250, 204, 21, 0.06);
            color: #fde047;
        }

        .nav-item.highlight:hover {
            background: rgba(250, 204, 21, 0.12);
            color: #fef08a;
        }

        .nav-item .icon {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        /* Main Content Container */
        #main-wrapper {
            flex: 1;
            display: flex;
            flex-direction: column;
            height: 100vh;
            overflow-y: auto;
            scroll-behavior: smooth;
        }

        .topbar {
            position: sticky;
            top: 0;
            background: rgba(22, 31, 46, 0.95);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-color);
            padding: 14px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 50;
        }

        .breadcrumb {
            font-size: 0.9rem;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .breadcrumb-active {
            color: var(--accent-blue);
            font-weight: 600;
        }

        .quick-actions {
            display: flex;
            gap: 10px;
        }

        .btn-action {
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 7px 16px;
            border-radius: 6px;
            font-size: 0.88rem;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.2s;
            font-family: inherit;
            font-weight: 500;
        }

        .btn-action:hover {
            border-color: var(--accent-blue);
            background: #27374f;
        }

        .content-container {
            max-width: 980px;
            width: 100%;
            margin: 0 auto;
            padding: 44px 50px 120px;
        }

        /* Markdown Body Styling */
        #article-body h1 {
            font-size: 2.3rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 2px solid var(--border-color);
            line-height: 1.35;
            scroll-margin-top: 80px;
        }

        #article-body h2 {
            font-size: 1.65rem;
            font-weight: 700;
            color: #ffffff;
            margin-top: 44px;
            margin-bottom: 18px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            scroll-margin-top: 80px;
        }

        #article-body h3 {
            font-size: 1.3rem;
            font-weight: 600;
            color: #e2e8f0;
            margin-top: 32px;
            margin-bottom: 14px;
            scroll-margin-top: 80px;
        }

        #article-body h4 {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--accent-purple);
            margin-top: 22px;
            margin-bottom: 10px;
            scroll-margin-top: 80px;
        }

        #article-body p {
            margin-bottom: 18px;
            color: #e2e8f0;
            font-size: 1.04rem;
            line-height: 1.85;
        }

        #article-body blockquote {
            margin: 24px 0;
            padding: 18px 22px;
            background-color: rgba(56, 189, 248, 0.08);
            border-left: 4px solid var(--accent-blue);
            border-radius: 0 10px 10px 0;
            color: #cbd5e1;
            font-size: 1.03rem;
        }

        #article-body blockquote p:last-child {
            margin-bottom: 0;
        }

        #article-body ul, #article-body ol {
            margin: 16px 0 22px 28px;
            color: #e2e8f0;
        }

        #article-body li {
            margin-bottom: 10px;
            line-height: 1.8;
        }

        #article-body strong {
            color: #ffffff;
            font-weight: 600;
        }

        .table-responsive {
            width: 100%;
            overflow-x: auto;
            margin: 28px 0;
        }

        #article-body table {
            width: 100%;
            border-collapse: collapse;
            background-color: var(--bg-secondary);
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }

        #article-body th {
            background-color: var(--bg-tertiary);
            color: #ffffff;
            text-align: left;
            padding: 14px 18px;
            font-weight: 600;
            font-size: 0.96rem;
            border-bottom: 2px solid var(--border-color);
        }

        #article-body td {
            padding: 14px 18px;
            border-bottom: 1px solid var(--border-color);
            color: #cbd5e1;
            font-size: 0.96rem;
            vertical-align: top;
        }

        #article-body tr:nth-child(even) td {
            background-color: rgba(255, 255, 255, 0.018);
        }

        #article-body tr:hover td {
            background-color: rgba(56, 189, 248, 0.05);
        }

        #article-body code {
            font-family: 'Fira Code', monospace;
            background: rgba(148, 163, 184, 0.16);
            padding: 2px 7px;
            border-radius: 5px;
            font-size: 0.88em;
            color: #f87171;
        }

        #article-body pre {
            background: #090d14;
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 20px;
            margin: 24px 0;
            overflow-x: auto;
        }

        #article-body pre code {
            background: transparent;
            padding: 0;
            color: #e2e8f0;
            font-size: 0.92rem;
        }

        #article-body hr {
            border: 0;
            height: 1px;
            background: var(--border-color);
            margin: 40px 0;
        }

        #article-body a {
            color: var(--accent-blue);
            text-decoration: none;
            border-bottom: 1px dashed rgba(56, 189, 248, 0.5);
            transition: all 0.2s;
            cursor: pointer;
        }

        #article-body a:hover {
            color: #7dd3fc;
            border-bottom-style: solid;
        }

        /* Next/Prev Navigation Footer */
        .lesson-footer-nav {
            display: flex;
            justify-content: space-between;
            margin-top: 60px;
            padding-top: 32px;
            border-top: 1px solid var(--border-color);
            gap: 20px;
        }

        .footer-nav-btn {
            display: flex;
            flex-direction: column;
            padding: 18px 24px;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            text-decoration: none;
            color: var(--text-primary);
            flex: 1;
            transition: all 0.2s;
            cursor: pointer;
        }

        .footer-nav-btn:hover {
            border-color: var(--accent-blue);
            background: var(--bg-tertiary);
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.25);
        }

        .footer-nav-btn.prev {
            align-items: flex-start;
        }

        .footer-nav-btn.next {
            align-items: flex-end;
            text-align: right;
        }

        .footer-nav-label {
            font-size: 0.8rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 4px;
            font-weight: 600;
        }

        .footer-nav-title {
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--accent-blue);
        }

        /* Mobile Hamburger */
        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: var(--text-primary);
            font-size: 1.6rem;
            cursor: pointer;
        }

        @media (max-width: 900px) {
            #sidebar {
                position: fixed;
                left: -100%;
                transition: left 0.3s ease;
            }
            #sidebar.open {
                left: 0;
            }
            .mobile-menu-btn {
                display: block;
            }
            .content-container {
                padding: 24px 20px 80px;
            }
            .topbar {
                padding: 12px 20px;
            }
        }
    </style>
</head>
<body>

    <!-- Sidebar Navigation -->
    <aside id="sidebar">
        <div class="brand">
            <div class="brand-title">
                <span>InvestSkill TH</span>
                <span class="brand-badge">ภาษาไทย 100%</span>
            </div>
            <div class="brand-subtitle">คลังความรู้ & กรอบการวิเคราะห์หุ้นสหรัฐฯ อย่างมืออาชีพ</div>
        </div>

        <div class="search-box">
            <input type="text" id="search-input" class="search-input" placeholder="🔍 ค้นหาคำศัพท์ หรือ หัวข้อ...">
        </div>

        <div class="nav-section">
            <div class="nav-heading">เครื่องมือ & คู่มือคำสั่ง</div>
            <a class="nav-item highlight" data-key="commands"><span class="icon">⚡</span> แนะนำทุกคำสั่ง (27 Skills)</a>
            <a class="nav-item" data-key="learning"><span class="icon">📖</span> แนะนำเส้นทางเรียนรู้ (Hub)</a>
            <a class="nav-item" data-key="concepts"><span class="icon">💡</span> แนวคิด & โมเดลความคิด</a>
            <a class="nav-item" data-key="glossary"><span class="icon">📚</span> พจนานุกรมศัพท์ A-Z</a>

            <div class="nav-heading">หลักสูตร 8 บทเรียน (Mastery Course)</div>
            <a class="nav-item" data-key="foundations"><span class="icon">1️⃣</span> 1. พื้นฐานการลงทุน</a>
            <a class="nav-item" data-key="statements"><span class="icon">2️⃣</span> 2. การอ่านงบการเงิน</a>
            <a class="nav-item" data-key="quality"><span class="icon">3️⃣</span> 3. คุณภาพธุรกิจ & Moat</a>
            <a class="nav-item" data-key="valuation"><span class="icon">4️⃣</span> 4. การประเมินมูลค่าหุ้น</a>
            <a class="nav-item" data-key="market"><span class="icon">5️⃣</span> 5. การอ่านสัญญาณตลาด</a>
            <a class="nav-item" data-key="portfolio"><span class="icon">6️⃣</span> 6. การจัดพอร์ต & ความเสี่ยง</a>
            <a class="nav-item" data-key="playbook"><span class="icon">7️⃣</span> 7. เพลย์บุ๊กมืออาชีพ (Case)</a>
            <a class="nav-item" data-key="case-amd"><span class="icon">8️⃣</span> 8. กรณีศึกษาหุ้น AMD</a>
        </div>
    </aside>

    <!-- Main Content -->
    <div id="main-wrapper">
        <div class="topbar">
            <div style="display:flex; align-items:center; gap:12px;">
                <button class="mobile-menu-btn" id="menu-toggle">☰</button>
                <div class="breadcrumb">
                    <span>InvestSkill</span>
                    <span>/</span>
                    <span class="breadcrumb-active" id="current-breadcrumb-title">กำลังโหลด...</span>
                </div>
            </div>
            <div class="quick-actions">
                <button class="btn-action" onclick="window.print()">🖨️ พิมพ์ / บันทึก PDF</button>
            </div>
        </div>

        <main class="content-container">
            <article id="article-body">
                <!-- Injected via Pure JS directly without external dependencies -->
            </article>

            <div class="lesson-footer-nav" id="lesson-footer-nav">
                <!-- Next/Prev buttons injected here -->
            </div>
        </main>
    </div>

    <!-- Pure Built-in Data (Zero Network CDN Dependency) -->
    <script>
        const ARTICLES = """ + articles_json + """;
        const LESSON_KEYS = ['commands', 'learning', 'concepts', 'glossary', 'foundations', 'statements', 'quality', 'valuation', 'market', 'portfolio', 'playbook', 'case-amd'];

        function scrollToAnchor(anchorId) {
            if (!anchorId) {
                document.getElementById('main-wrapper').scrollTo({ top: 0, behavior: 'smooth' });
                return;
            }
            setTimeout(() => {
                const target = document.getElementById(anchorId);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }, 60);
        }

        function renderPage(key, targetAnchor = null) {
            if (!ARTICLES[key]) key = 'commands';
            
            // Update active sidebar item
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.toggle('active', item.dataset.key === key);
            });

            const lesson = ARTICLES[key];
            document.getElementById('current-breadcrumb-title').textContent = lesson.title;
            document.title = lesson.title + ' — InvestSkill TH';

            // Direct HTML insertion
            document.getElementById('article-body').innerHTML = lesson.html;

            // Render Prev / Next Buttons
            const currentIndex = LESSON_KEYS.indexOf(key);
            let footerHtml = '';
            
            if (currentIndex > 0) {
                const prevKey = LESSON_KEYS[currentIndex - 1];
                footerHtml += `
                    <div class="footer-nav-btn prev" onclick="navigateTo('${prevKey}')">
                        <div class="footer-nav-label">← หน้าก่อนหน้า</div>
                        <div class="footer-nav-title">${ARTICLES[prevKey].title}</div>
                    </div>
                `;
            } else {
                footerHtml += '<div></div>';
            }

            if (currentIndex < LESSON_KEYS.length - 1) {
                const nextKey = LESSON_KEYS[currentIndex + 1];
                footerHtml += `
                    <div class="footer-nav-btn next" onclick="navigateTo('${nextKey}')">
                        <div class="footer-nav-label">หน้าถัดไป →</div>
                        <div class="footer-nav-title">${ARTICLES[nextKey].title}</div>
                    </div>
                `;
            }

            document.getElementById('lesson-footer-nav').innerHTML = footerHtml;

            // Scroll into view
            scrollToAnchor(targetAnchor);
        }

        function navigateTo(key, anchor = null) {
            window.location.hash = anchor ? `${key}:${anchor}` : key;
        }

        function handleHashChange() {
            let hash = window.location.hash.replace('#', '');
            if (!hash) hash = 'commands';
            
            let [key, anchor] = hash.split(':');
            renderPage(key, anchor);
        }

        // Attach click listeners to sidebar nav items
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', () => {
                navigateTo(item.dataset.key);
                document.getElementById('sidebar').classList.remove('open');
            });
        });

        // Search Filter
        document.getElementById('search-input').addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            document.querySelectorAll('.nav-item').forEach(item => {
                const text = item.textContent.toLowerCase();
                item.style.display = text.includes(query) ? 'flex' : 'none';
            });
        });

        // Mobile menu toggle
        document.getElementById('menu-toggle').addEventListener('click', () => {
            document.getElementById('sidebar').classList.toggle('open');
        });

        // Listen for internal anchor clicks
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a');
            if (link && link.getAttribute('href') && link.getAttribute('href').startsWith('#')) {
                const rawHref = link.getAttribute('href').replace('#', '');
                e.preventDefault();
                if (rawHref.includes(':')) {
                    const [pageKey, anchorId] = rawHref.split(':');
                    navigateTo(pageKey, anchorId);
                } else if (ARTICLES[rawHref]) {
                    navigateTo(rawHref);
                } else {
                    // Internal on-page anchor jump
                    scrollToAnchor(rawHref);
                }
            }
        });

        window.addEventListener('hashchange', handleHashChange);
        window.addEventListener('DOMContentLoaded', handleHashChange);
        // Direct initial trigger
        handleHashChange();
    </script>
</body>
</html>
"""

with open('site/learning-th.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Rebuilt site/learning-th.html with working Anchor Jump & Smooth Scroll!")
