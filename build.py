#!/usr/bin/env python3
"""Build script: Parses content PRDs, generates index.html"""
import re, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BRAIN_DIR = os.path.join(SCRIPT_DIR, '..', '..', '.gemini', 'antigravity', 'brain', 'f1f65c89-93d3-4722-b1a6-60b30db5fcae')
if not os.path.exists(BRAIN_DIR):
    BRAIN_DIR = r'C:\Users\User\.gemini\antigravity\brain\f1f65c89-93d3-4722-b1a6-60b30db5fcae'

SUBJECTS = {
    "math": {
        "title": "Math",
        "prd": os.path.join(BRAIN_DIR, 'content_prd.md'),
        "overview": os.path.join(SCRIPT_DIR, 'pdf_text.txt'),
        "categories": {
            "Algebra & Equations": [1,2,3,4,9,10,30,38,39,40,41,42,43,47],
            "Geometry & Measurement": [13,14,15,16,17,18],
            "Graphs, Slope & Functions": [5,6,7,8,26,27,28,29,46],
            "Data, Stats & Probability": [25,32,33,34,35],
            "Numbers & Percents": [11,12,19,20,21,22,23,24,31,36,37,44,45,48,49,50],
        },
        "cat_ids": {
            "Algebra & Equations": "math-algebra",
            "Geometry & Measurement": "math-geometry",
            "Graphs, Slope & Functions": "math-graphs",
            "Data, Stats & Probability": "math-data",
            "Numbers & Percents": "math-numbers",
        }
    },
    "science": {
        "title": "Science",
        "prd": os.path.join(BRAIN_DIR, 'science_content_prd.md'),
        "overview": os.path.join(SCRIPT_DIR, 'science_pdf_text.txt'),
        "categories": {
            "Scientific Method & Data": [1,2,3,4,44,45,46,47,48,49,50],
            "Life Science": [5,6,7,8,9,10,11,12,13,14,15],
            "Physical Science": [16,17,18,19,20,21,22,23,24,25,34,35,36],
            "Earth & Space Science": [26,27,28,29,30,31,32,33,37,38,39,40,41,42,43],
        },
        "cat_ids": {
            "Scientific Method & Data": "sci-method",
            "Life Science": "sci-life",
            "Physical Science": "sci-physical",
            "Earth & Space Science": "sci-earth",
        }
    },
    "social_studies": {
        "title": "Social Studies",
        "prd": os.path.join(BRAIN_DIR, 'social_studies_content_prd.md'),
        "overview": os.path.join(SCRIPT_DIR, 'social_studies_pdf_text.txt'),
        "categories": {
            "Civics & Government": [1,2,3,4,5,6,7,8,26,27,28,29,30,31,37,38,39,40],
            "US History": [9,10,11,12,13,14,15,16,36,43,44,45,46],
            "Economics": [17,18,19,20,24,25,33,41],
            "Geography & Global Issues": [21,22,23,32,34,35,42,47,48,49,50],
        },
        "cat_ids": {
            "Civics & Government": "ss-civics",
            "US History": "ss-history",
            "Economics": "ss-economics",
            "Geography & Global Issues": "ss-geography",
        }
    },
    "rla": {
        "title": "Reading & Language Arts",
        "prd": os.path.join(SCRIPT_DIR, 'GED_RLA_content.md'),
        "overview": os.path.join(SCRIPT_DIR, 'rla_pdf_text.txt'),
        "categories": {
            "Absolute Words": [1,2,3,4,5,6,7,8,9,10],
            "Emotional Language": [11,12,13,14,15,16,17,18,19,20],
            "Unsupported Comparisons": [21,22,23,24,25,26,27,28,29,30],
            "Half-Right, All-Wrong": [31,32,33,34,35,36,37,38,39,40],
        },
        "cat_ids": {
            "Absolute Words": "rla-absolute",
            "Emotional Language": "rla-emotional",
            "Unsupported Comparisons": "rla-comparisons",
            "Half-Right, All-Wrong": "rla-halfright",
        }
    }
}

def bold_to_strong(text):
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

def parse_questions(md_text):
    parts = re.split(r'^## Question ', md_text, flags=re.MULTILINE)
    questions = {}
    for part in parts[1:]:
        m = re.match(r'(\d+):\s*(.*?)$', part, re.MULTILINE)
        if m:
            qnum = int(m.group(1))
            qtitle = m.group(2).strip()
            body = part[m.end():]
            questions[qnum] = {"num": qnum, "title": qtitle, "body": body}
    return questions

def md_to_html_body(body):
    lines = body.strip().split('\n')
    html_parts = []
    i = 0
    practice_count = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('### 💡 Core Concept') or line.startswith('### 💡 Core Science Concept') or line.startswith('### 💡 Core Social Studies Concept') or line.startswith('### 💡 Core RLA Concept'):
            i += 1
            concept_lines = []
            while i < len(lines) and not lines[i].strip().startswith('### '):
                if lines[i].strip():
                    concept_lines.append(lines[i].strip())
                i += 1
            html_parts.append(bold_to_strong(f'<div class="callout tip"><div class="callout-title">💡 CORE CONCEPT</div><p>{" ".join(concept_lines)}</p></div>'))
            continue
        if line.startswith('### 📝 Step-by-Step Solution') or line.startswith('### 🔬 Detailed Explanation & Breakdown') or line.startswith('### 📜 Context & Explanation'):
            i += 1
            html_parts.append(f'<h3>{line.replace("### ", "")}</h3>')
            while i < len(lines) and not lines[i].strip().startswith('### '):
                sline = lines[i].strip()
                if not sline:
                    i += 1
                    continue
                if sline.startswith('![') and '](' in sline:
                    m_img = re.match(r'!\[(.*?)\]\((.*?)\)', sline)
                    if m_img:
                        html_parts.append(f'<img src="{m_img.group(2)}" alt="{m_img.group(1)}" class="content-img">')
                elif sline.startswith('* **Step') or sline.startswith('* **Final Answer') or sline.startswith('- **Key Process') or sline.startswith('- **Why it matters') or sline.startswith('- **Formula Used') or sline.startswith('- **Step-by-Step') or sline.startswith('- **Final Answer') or sline.startswith('* **Historical Background') or sline.startswith('* **Why It Matters Today') or sline.startswith('* **Key Definition') or sline.startswith('* **How to Read') or sline.startswith('* **Strategy Reminder'):
                    html_parts.append(bold_to_strong(f'<p class="step-item">{sline[2:]}</p>'))
                elif sline.startswith('$$') and sline.endswith('$$'):
                    html_parts.append(f'<p class="math-display">{sline}</p>')
                else:
                    html_parts.append(bold_to_strong(f'<p>{sline}</p>'))
                i += 1
            continue
        if line.startswith('### 🧠 GED Practice Problems'):
            i += 1
            practice_count = 0
            continue
        if line.startswith('#### Practice'):
            practice_count += 1
            i += 1
            q_text = []
            options = []
            answer_text = ""
            while i < len(lines):
                pline = lines[i].strip()
                if not pline:
                    i += 1
                    continue
                if pline.startswith('#### Practice') or pline.startswith('### ') or pline.startswith('## ') or pline == '---':
                    break
                if pline.startswith('* **A)') or pline.startswith('* **B)') or pline.startswith('* **C)') or pline.startswith('* **D)') or pline.startswith('- **A)') or pline.startswith('- **B)') or pline.startswith('- **C)') or pline.startswith('- **D)'):
                    options.append(pline[3:].strip() if pline.startswith('-') else pline[2:].strip())
                elif pline.startswith('* **Answer:') or pline.startswith('- **Answer:'):
                    answer_text = pline[3:].strip() if pline.startswith('-') else pline[2:].strip()
                else:
                    q_text.append(pline)
                i += 1
            opts_html = "".join(f'<li>{bold_to_strong(o)}</li>' for o in options)
            html_parts.append(bold_to_strong(f'''<div class="practice-box">
<div class="practice-header">🧠 Practice {practice_count}</div>
<div class="practice-body">
<div class="practice-question"><p>{" ".join(q_text)}</p><ul class="content-list">{opts_html}</ul></div>
<button class="show-answer-btn" onclick="this.style.display='none'; this.nextElementSibling.classList.add('show');">Show Answer</button>
<div class="practice-answer"><p>{answer_text}</p></div>
</div></div>'''))
            continue
        if line == '---' or not line:
            i += 1
            continue
        i += 1
    return '\n'.join(html_parts)

def build_overview(pdf_path):
    with open(pdf_path, 'r', encoding='utf-8') as f:
        raw = f.read()
    lines = [l.strip() for l in raw.strip().split('\n') if l.strip()]
    items = []
    for l in lines:
        m = re.match(r'^(\d+)\.\s*(.*)', l)
        if m:
            items.append(f'<li><span class="overview-num">{m.group(1)}.</span> {m.group(2)}</li>')
    return '\n'.join(items)

def build_html():
    
    subject_htmls = {}

    for subj_key, subj_data in SUBJECTS.items():
        with open(subj_data["prd"], 'r', encoding='utf-8') as f:
            questions = parse_questions(f.read())
        
        overview_items = build_overview(subj_data["overview"])

        # Build category tabs
        cat_btns = [f'<button class="cat-btn active" data-cat="{subj_key}-overview">Question Overview</button>']
        cat_panes = []

        # Overview pane
        cat_panes.append(f'''<div id="cat-{subj_key}-overview" class="cat-pane active">
<div class="container">
<div class="overview-section">
<div class="section-header"><span class="section-number">OVERVIEW</span><h2>{len([q for cat_qs in subj_data["categories"].values() for q in cat_qs])} Most Important {subj_data["title"]} Questions</h2></div>
<ol class="overview-list">{overview_items}</ol>
</div></div></div>''')

        for cat_name, cat_id in subj_data["cat_ids"].items():
            q_nums = subj_data["categories"][cat_name]
            cat_btns.append(f'<button class="cat-btn" data-cat="{cat_id}">{cat_name}</button>')
            sub_btns = []
            sub_panes = []
            for idx, qn in enumerate(q_nums):
                q = questions.get(qn)
                if not q: continue
                active = ' active' if idx == 0 else ''
                sub_btns.append(f'<button class="tab-btn{active}" data-target="{cat_id}-q{qn}">Q{qn}</button>')
                body_html = md_to_html_body(q["body"])
                title_html = bold_to_strong(q["title"])
                formula_btn = '''<button class="formula-btn" onclick="document.getElementById('formulaModal').classList.add('show')" aria-label="Formula Sheet">📐</button>''' if subj_key == 'math' else ''
                sub_panes.append(f'''<div class="section tab-pane{active}" id="{cat_id}-q{qn}">
<div class="section-header"><span class="section-number">QUESTION {qn}</span><h2>{title_html}</h2>{formula_btn}</div>
{body_html}
</div>''')
            tabs_nav = '\n'.join(sub_btns)
            panes = '\n'.join(sub_panes)
            cat_panes.append(f'''<div id="cat-{cat_id}" class="cat-pane">
<div class="container">
<div class="tabs-wrapper" id="wrapper-{cat_id}">
<button class="scroll-btn" onclick="this.nextElementSibling.scrollBy({{left:-200,behavior:'smooth'}})">&lsaquo;</button>
<nav class="tabs-nav">{tabs_nav}</nav>
<button class="scroll-btn" onclick="this.previousElementSibling.scrollBy({{left:200,behavior:'smooth'}})">&rsaquo;</button>
</div>
{panes}
</div></div>''')

        cat_btns_html = '\n'.join(cat_btns)
        cat_panes_html = '\n'.join(cat_panes)
        
        display_style = 'block' if subj_key == 'math' else 'none'
        
        subject_htmls[subj_key] = f'''
<!-- SUBJECT CONTAINER: {subj_key.upper()} -->
<div id="subject-{subj_key}" class="subject-container" style="display: {display_style};">
<div class="cat-nav-wrapper">
<button class="cat-scroll-btn" onclick="this.nextElementSibling.scrollBy({{left:-200,behavior:'smooth'}})">&lsaquo;</button>
<nav class="cat-nav" id="catNav-{subj_key}">{cat_btns_html}</nav>
<button class="cat-scroll-btn" onclick="this.previousElementSibling.scrollBy({{left:200,behavior:'smooth'}})">&rsaquo;</button>
</div>
{cat_panes_html}
</div>
'''

    final_html = f'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GED Study Guide - Math, Science, Social Studies & RLA</title>
<meta name="description" content="Master the most important GED questions in Math, Science, Social Studies and Reading & Language Arts with step-by-step solutions, explanations, and interactive practice problems.">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'$',right:'$',display:false}}],throwOnError:false}});"></script>
<style>
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
:root{{--transition-speed:0.3s}}
[data-theme="dark"]{{
--bg-primary:#000;--bg-secondary:#0a0a0a;--bg-card:#111;--bg-code:#1a1a1a;
--bg-tip:rgba(255,255,255,0.04);--bg-important:rgba(255,255,255,0.04);--bg-note:rgba(255,255,255,0.04);
--text-primary:#fff;--text-secondary:#a0a0a0;--text-muted:#666;
--accent:#fff;--border:#222;--border-light:#1a1a1a;
--tip-border:#3b82f6;--important-border:#f59e0b;--note-border:#8b5cf6;--caution-border:#ef4444;
--scrollbar-thumb:#333;--scrollbar-track:#111;--toggle-bg:#222;--toggle-knob:#fff;
--shadow:0 1px 3px rgba(0,0,0,0.5)}}
[data-theme="light"]{{
--bg-primary:#fff;--bg-secondary:#f8f8f8;--bg-card:#fff;--bg-code:#f5f5f5;
--bg-tip:rgba(0,0,0,0.03);--bg-important:rgba(0,0,0,0.03);--bg-note:rgba(0,0,0,0.03);
--text-primary:#000;--text-secondary:#555;--text-muted:#999;
--accent:#000;--border:#e0e0e0;--border-light:#eee;
--tip-border:#2563eb;--important-border:#d97706;--note-border:#7c3aed;--caution-border:#dc2626;
--scrollbar-thumb:#ccc;--scrollbar-track:#f0f0f0;--toggle-bg:#e0e0e0;--toggle-knob:#000;
--shadow:0 1px 3px rgba(0,0,0,0.1)}}
body{{font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;background:var(--bg-primary);color:var(--text-secondary);line-height:1.7;-webkit-font-smoothing:antialiased;transition:background var(--transition-speed),color var(--transition-speed)}}
::-webkit-scrollbar{{width:6px}}::-webkit-scrollbar-track{{background:var(--scrollbar-track)}}::-webkit-scrollbar-thumb{{background:var(--scrollbar-thumb);border-radius:3px}}
/* === TOP NAV (Tier 1) === */
.top-level-nav{{position:sticky;top:0;z-index:200;display:flex;align-items:center;justify-content:space-between;padding:10px 24px;background:var(--bg-primary);border-bottom:2px solid var(--border);transition:background var(--transition-speed),border var(--transition-speed)}}
.top-nav-left{{display:flex;align-items:center;gap:10px}}
.master-tab{{background:transparent;border:2px solid transparent;color:var(--text-muted);font-size:0.9rem;font-weight:700;padding:8px 20px;border-radius:8px;cursor:pointer;font-family:inherit;transition:all 0.2s}}
.master-tab:hover{{color:var(--text-primary);background:var(--bg-code)}}
.master-tab.active{{border-color:var(--accent);color:var(--text-primary);box-shadow:var(--shadow);background:transparent}}
.top-nav-right{{display:flex;align-items:center;gap:12px}}
.theme-toggle{{width:52px;height:28px;border-radius:14px;background:var(--toggle-bg);border:none;cursor:pointer;position:relative;transition:background var(--transition-speed);flex-shrink:0;overflow:hidden}}
.theme-toggle::after{{content:'';position:absolute;width:22px;height:22px;border-radius:50%;background:var(--toggle-knob);top:3px;left:3px;transition:transform var(--transition-speed);z-index:2}}
[data-theme="light"] .theme-toggle::after{{transform:translateX(24px)}}
.toggle-icon{{position:absolute;top:50%;transform:translateY(-50%);font-size:0.75rem;pointer-events:none;z-index:1;transition:opacity var(--transition-speed);line-height:1}}
.toggle-moon{{left:6px}}
.toggle-sun{{right:5px}}
[data-theme="dark"] .toggle-moon{{opacity:0}}
[data-theme="dark"] .toggle-sun{{opacity:1}}
[data-theme="light"] .toggle-moon{{opacity:1}}
[data-theme="light"] .toggle-sun{{opacity:0}}
/* === CATEGORY NAV (Tier 2) === */
.cat-nav-wrapper{{position:sticky;top:50px;z-index:190;background:var(--bg-primary);border-bottom:1px solid var(--border);transition:background var(--transition-speed),border var(--transition-speed);display:flex;align-items:center;overflow:hidden}}
.cat-nav{{display:flex;overflow-x:auto;white-space:nowrap;scrollbar-width:none;-webkit-overflow-scrolling:touch;flex:1;padding:0 16px}}
.cat-nav::-webkit-scrollbar{{display:none}}
.cat-btn{{padding:10px 18px;font-size:0.8rem;font-weight:600;color:var(--text-muted);background:transparent;border:none;border-bottom:2px solid transparent;cursor:pointer;transition:all var(--transition-speed);font-family:inherit;white-space:nowrap}}
.cat-btn:hover{{color:var(--text-secondary);background:var(--bg-code)}}
.cat-btn.active{{color:var(--text-primary);border-bottom-color:var(--accent)}}
.cat-scroll-btn{{width:32px;height:100%;display:flex;align-items:center;justify-content:center;background:var(--bg-primary);border:none;color:var(--text-muted);cursor:pointer;font-size:1rem;flex-shrink:0;transition:color var(--transition-speed)}}
.cat-scroll-btn:hover{{color:var(--text-primary)}}
/* === CATEGORY PANES === */
.cat-pane{{display:none}}.cat-pane.active{{display:block;animation:fadeIn 0.3s ease-in-out}}
.container{{max-width:780px;margin:0 auto;padding:40px 24px 80px}}
/* === QUESTION TABS (Tier 3) === */
.tabs-wrapper{{display:flex;align-items:center;margin-bottom:32px;border-bottom:1px solid var(--border);position:relative}}
.tabs-nav{{display:flex;overflow-x:auto;white-space:nowrap;scrollbar-width:none;-webkit-overflow-scrolling:touch;flex:1}}
.tabs-nav::-webkit-scrollbar{{display:none}}
.tab-btn{{padding:12px 20px;font-size:0.9rem;font-weight:600;color:var(--text-muted);background:transparent;border:none;border-bottom:2px solid transparent;cursor:pointer;transition:all var(--transition-speed);font-family:inherit;white-space:nowrap}}
.tab-btn:hover{{color:var(--text-secondary);background:var(--bg-code)}}
.tab-btn.active{{color:var(--text-primary);border-bottom:2px solid var(--accent)}}
.scroll-btn{{width:36px;height:36px;display:flex;align-items:center;justify-content:center;background:transparent;border:none;color:var(--text-muted);cursor:pointer;font-size:1.2rem;flex-shrink:0;transition:color var(--transition-speed)}}
.scroll-btn:hover{{color:var(--text-primary)}}
/* === SECTIONS === */
.section{{margin-bottom:56px}}.tab-pane{{display:none}}.tab-pane.active{{display:block;animation:fadeIn 0.3s ease-in-out}}
.section-header{{display:flex;align-items:center;gap:12px;padding-bottom:12px;border-bottom:1px solid var(--border);margin-bottom:20px;flex-wrap:wrap}}
.section-number{{font-size:0.75rem;font-weight:700;color:var(--text-muted);background:var(--bg-code);border:1px solid var(--border);padding:4px 10px;border-radius:4px;text-transform:uppercase;letter-spacing:0.05em;white-space:nowrap}}
.section-header h2{{font-size:1.4rem;font-weight:700;letter-spacing:-0.02em;color:var(--text-primary);flex:1}}
.formula-btn{{background:transparent;border:1px solid var(--border);border-radius:6px;padding:4px 10px;cursor:pointer;font-size:1rem;color:var(--text-muted);transition:all var(--transition-speed);flex-shrink:0}}
.formula-btn:hover{{color:var(--text-primary);border-color:var(--text-muted);background:var(--bg-code)}}
h3{{font-size:1.1rem;font-weight:600;letter-spacing:-0.01em;margin:28px 0 12px;color:var(--text-primary)}}
h4{{font-size:1rem;font-weight:600;margin:20px 0 10px;color:var(--text-primary)}}
p{{margin-bottom:12px}}strong{{font-weight:600;color:var(--text-primary)}}
.content-img{{max-width:100%;height:auto;border-radius:8px;margin:20px 0;display:block;border:1px solid var(--border)}}
.callout{{border-left:3px solid var(--tip-border);border-radius:0 8px 8px 0;padding:16px 20px;margin:20px 0;font-size:0.9rem;background:var(--bg-tip)}}
.callout-title{{font-weight:800;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.05em;color:var(--tip-border);margin-bottom:6px}}
.step-item{{position:relative;padding-left:16px;margin-bottom:10px}}
.step-item::before{{content:'';position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--text-muted)}}
.math-display{{overflow-x:auto;padding:15px;background:var(--bg-code);border-radius:6px;margin:15px 0;text-align:center}}
ul.content-list{{list-style:none;margin-left:0;margin-bottom:15px}}
ul.content-list li{{position:relative;padding-left:20px;margin-bottom:8px}}
ul.content-list li::before{{content:'\\2022';position:absolute;left:0;color:var(--accent);font-weight:bold}}
.practice-box{{margin-top:28px;border:1px solid var(--note-border);border-radius:8px;overflow:hidden;background:var(--bg-card)}}
.practice-header{{background:var(--bg-secondary);padding:12px 16px;font-weight:700;font-size:1rem;border-bottom:1px solid var(--border);color:var(--note-border)}}
.practice-body{{padding:20px}}.practice-question{{font-size:0.95rem;margin-bottom:15px;line-height:1.5}}.practice-question p{{margin-bottom:10px}}
.show-answer-btn{{background:var(--note-border);color:#fff;border:none;padding:10px 18px;border-radius:6px;font-weight:600;cursor:pointer;font-family:inherit;font-size:0.9rem;transition:opacity var(--transition-speed)}}
.show-answer-btn:hover{{opacity:0.85}}
.practice-answer{{display:none;margin-top:20px;padding-top:15px;border-top:1px dashed var(--border)}}.practice-answer.show{{display:block}}
/* === OVERVIEW === */
.overview-section{{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;overflow:hidden;box-shadow:var(--shadow)}}
.overview-section .section-header{{padding:20px;margin:0;background:var(--bg-secondary)}}
.overview-list{{list-style:none;padding:0;counter-reset:none}}
.overview-list li{{padding:12px 16px;border-bottom:1px solid var(--border);font-size:0.95rem;color:var(--text-secondary);display:flex;gap:10px;transition:background var(--transition-speed)}}
.overview-list li:hover{{background:var(--bg-code)}}
.overview-num{{font-weight:700;color:var(--text-primary);min-width:28px}}
/* === FORMULA MODAL === */
.formula-modal{{display:none;position:fixed;top:0;left:0;width:100%;height:100%;z-index:9999;background:rgba(0,0,0,0.85);justify-content:center;padding:20px;overflow-y:auto}}
.formula-modal.show{{display:flex}}
.formula-modal-inner{{position:relative;max-width:900px;width:100%;margin:auto}}
.formula-modal-inner img{{width:100%;height:auto;border-radius:8px;display:block}}
.formula-close{{position:sticky;top:0;float:right;margin-right:-18px;margin-top:-10px;width:36px;height:36px;border-radius:50%;background:#ef4444;border:none;color:#fff;font-size:1.2rem;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,0.4);transition:transform 0.2s;z-index:10}}
.formula-close:hover{{transform:scale(1.1)}}
@keyframes fadeIn{{from{{opacity:0;transform:translateY(5px)}}to{{opacity:1;transform:translateY(0)}}}}
@media(max-width:640px){{
.top-level-nav{{padding:8px 12px}}
.master-tab{{font-size:0.8rem;padding:6px 14px}}
.cat-btn{{font-size:0.72rem;padding:8px 12px}}
.cat-scroll-btn{{display:none}}
.container{{padding:24px 16px 60px}}
.section{{margin-bottom:40px}}
.section-header{{flex-direction:row;gap:8px}}
.section-header h2{{font-size:1.15rem}}
.callout{{padding:14px 16px}}
.scroll-btn{{display:none}}
.tab-btn{{padding:10px 14px;font-size:0.8rem}}
.formula-modal-inner{{max-width:95vw}}
.formula-close{{width:30px;height:30px;font-size:1rem;margin-right:-8px}}
}}
@media(max-width:380px){{
.master-tab{{font-size:0.72rem;padding:5px 10px}}
.cat-btn{{font-size:0.65rem;padding:6px 8px}}
}}
</style>
</head>
<body>
<!-- Tier 1: Top Nav -->
<div class="top-level-nav">
<div class="top-nav-left">
<button class="master-tab active" data-subject="math">Math</button>
<button class="master-tab" data-subject="science">Science</button>
<button class="master-tab" data-subject="social_studies">Social Studies</button>
<button class="master-tab" data-subject="rla">Language Arts</button>
</div>
<div class="top-nav-right"><button class="theme-toggle" id="themeToggle" aria-label="Toggle theme"><span class="toggle-icon toggle-moon">🌙</span><span class="toggle-icon toggle-sun">☀️</span></button></div>
</div>

{subject_htmls["math"]}
{subject_htmls["science"]}
{subject_htmls["social_studies"]}
{subject_htmls["rla"]}

<!-- Formula Modal -->
<div class="formula-modal" id="formulaModal">
<div class="formula-modal-inner">
<button class="formula-close" onclick="document.getElementById('formulaModal').classList.remove('show')">&times;</button>
<img src="math_formula_sheet_page-0001.jpg" alt="GED Math Formula Sheet">
</div>
</div>

<script>
// Theme Toggle
const toggleBtn = document.getElementById('themeToggle');
const htmlEl = document.documentElement;
const savedTheme = localStorage.getItem('theme') || 'dark';
htmlEl.setAttribute('data-theme', savedTheme);
toggleBtn.addEventListener('click', () => {{
    const current = htmlEl.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    htmlEl.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
}});

// Master Tab Logic
const masterTabs = document.querySelectorAll('.master-tab');
masterTabs.forEach(tab => {{
    tab.addEventListener('click', () => {{
        masterTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        const subject = tab.getAttribute('data-subject');
        document.querySelectorAll('.subject-container').forEach(c => c.style.display = 'none');
        document.getElementById('subject-' + subject).style.display = 'block';
    }});
}});

// Category Tabs Logic
document.querySelectorAll('.cat-btn').forEach(btn => {{
    btn.addEventListener('click', () => {{
        const container = btn.closest('.subject-container');
        container.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const catId = btn.getAttribute('data-cat');
        container.querySelectorAll('.cat-pane').forEach(p => p.classList.remove('active'));
        container.querySelector('#cat-' + catId).classList.add('active');
        btn.scrollIntoView({{behavior:'smooth', block:'nearest', inline:'center'}});
    }});
}});

// Question Tabs Logic
document.querySelectorAll('.tab-btn').forEach(btn => {{
    btn.addEventListener('click', () => {{
        const wrapper = btn.closest('.tabs-wrapper');
        const paneId = btn.getAttribute('data-target');
        const parentPane = btn.closest('.cat-pane');
        wrapper.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        parentPane.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
        document.getElementById(paneId).classList.add('active');
        btn.scrollIntoView({{behavior:'smooth', block:'nearest', inline:'center'}});
    }});
}});
</script>
</body>
</html>'''
    
    out_path = os.path.join(SCRIPT_DIR, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print(f"Generated index.html ({len(final_html)} bytes)")

if __name__ == '__main__':
    build_html()
