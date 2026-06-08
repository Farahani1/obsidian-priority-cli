import re
import os
from pathlib import Path
from datetime import datetime
import math
from typing import Dict, Optional

def normalize_score(score: str) -> float:
    """Normalize score from 1-5 to [0,1]. Empty/missing -> 0.0 (lowest)"""
    if not score or str(score).strip() in ['', '[]', ' ', 'due::']:
        return 0.0
    try:
        val = float(str(score).strip())
        return max(0.0, min(1.0, (val - 1) / 4))  # 1→0, 5→1
    except (ValueError, TypeError):
        return 0.0


def parse_due_date(due_str: str) -> float:
    """Return days left until due date. Empty/invalid -> 365 (very low urgency)"""
    if not due_str or str(due_str).strip() in ['', '[]', ' ', 'due::']:
        return 365.0
    
    due_str = str(due_str).strip().replace('[due::', '').replace(']', '').strip()
    if not due_str:
        return 365.0
    
    try:
        for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%m/%d/%Y', '%Y.%m.%d']:
            try:
                due_date = datetime.strptime(due_str, fmt).date()
                today = datetime.now().date()
                days_left = (due_date - today).days
                return max(0.0, days_left)
            except ValueError:
                continue
        return 365.0
    except Exception:
        return 365.0


def compute_priority(load: str, force: str, necessity: str, value: str, due: str, params: Optional[Dict] = None) -> float:
    if params is None:
        params = {
            'alpha': 2.0, 'beta': 2.0, 'gamma': 2.5, 'delta': 1.5,
            'w_L': 0.8, 'w_F': 1.5, 'k': 10.0, 'theta': 0.6
        }
    
    L = normalize_score(load)
    F = normalize_score(force)
    N = normalize_score(necessity)
    V = normalize_score(value)
    D = parse_due_date(due)
    
    # Urgency
    U = (1 / (D + 1) ** params['alpha']) * (1 + params['beta'] * N)
    
    # Strategic importance
    S = N ** params['gamma'] + (1 - N) * (V ** params['delta'])
    
    # Execution friction
    E = math.exp( - (params['w_L'] * L + params['w_F'] * F) )
    
    priority = U * S * E
    
    # Doability gate
    G = 1 / (1 + math.exp(params['k'] * (F - params['theta'])))
    
    return round(priority * G, 4)


def extract_task_fields(line: str) -> Dict[str, str]:
    """Extract fields from a task line"""
    fields = {
        'id': '', 'title': '', 'stage': '', 'force': '', 
        'load': '', 'necessity': '', 'value': '', 'due': ''
    }
    
    for key in fields:
        match = re.search(rf'\[{key}::\s*(.*?)\]', line)
        if match:
            fields[key] = match.group(1).strip()
    
    # Extract title if missing
    if not fields['title']:
        title_match = re.search(r'-\s*\[\s*\]\s*(.+?)(?:\s+#task|\s+\[)', line)
        if title_match:
            fields['title'] = title_match.group(1).strip()
    
    return fields


def process_vault(vault_path: str):
    vault_path = Path(vault_path)
    if not vault_path.is_dir():
        print(f"Error: {vault_path} is not a valid directory.")
        return
    
    # Updated regex for - [ ] tasks
    task_pattern = re.compile(r'^\s*-\s*\[\s*\].*?#task', re.MULTILINE)
    
    updated_count = 0
    total_tasks = 0
    
    print(f"Scanning vault: {vault_path}")
    
    for md_file in vault_path.rglob("*.md"):
        try:
            content = md_file.read_text(encoding='utf-8')
            original_content = content
            offset = 0
            
            for match in task_pattern.finditer(content):
                start = match.start() + offset
                line_end = content.find('\n', start)
                if line_end == -1:
                    line_end = len(content)
                
                task_line = content[start:line_end]
                fields = extract_task_fields(task_line)
                total_tasks += 1
                
                prio = compute_priority(
                    fields['load'], fields['force'],
                    fields['necessity'], fields['value'],
                    fields['due']
                )
                
                if '[priority::' not in task_line:
                    new_field = f' [priority:: {prio}]'
                    updated_line = task_line.rstrip() + new_field
                    
                    content = content[:start] + updated_line + content[line_end:]
                    offset += len(new_field)
                    updated_count += 1
                    
                    print(f"✓ Updated: {fields['title'] or 'Untitled'} → Priority: {prio} | {md_file.name}")
                else:
                    print(f"→ Already has priority: {fields['title'] or 'Untitled'}")
            
            if content != original_content:
                md_file.write_text(content, encoding='utf-8')
                
        except Exception as e:
            print(f"Error processing {md_file.name}: {e}")
    
    print("\n" + "="*70)
    print(f"✅ Task priority update finished!")
    print(f"   Total tasks found : {total_tasks}")
    print(f"   Tasks updated     : {updated_count}")
    print("="*70)


if __name__ == "__main__":
    # ←←← CHANGE THIS TO YOUR ACTUAL VAULT PATH ←←←
    your_vault_path = r"C:\path\to\your\obsidian\vault"   # Windows example
    # your_vault_path = "/Users/yourname/vault"           # macOS / Linux example
    
    if "your/obsidian/vault" in your_vault_path or not your_vault_path:
        print("⚠️  Please edit the script and set your actual Obsidian vault path!")
    else:
        process_vault(your_vault_path)