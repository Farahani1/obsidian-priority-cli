import re
import argparse
from pathlib import Path
from datetime import datetime
import math
from typing import Dict, Optional

def normalize_score(score: str) -> float:
    """Normalize 1-5 → [0,1]. Empty/missing → 0.0 (low importance)"""
    if not score or str(score).strip() in ['', '[]', ' ', 'due::']:
        return 0.0
    try:
        val = float(str(score).strip())
        return max(0.0, min(1.0, (val - 1) / 4))
    except:
        return 0.0


def parse_due_date(due_str: str) -> float:
    """Days left. Empty → 30 (moderate urgency)"""
    if not due_str or str(due_str).strip() in ['', '[]', ' ', 'due::']:
        return 30.0
    
    due_str = str(due_str).strip().replace('[due::', '').replace(']', '').strip()
    if not due_str:
        return 30.0
    
    try:
        for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d', '%m/%d/%Y', '%Y.%m.%d']:
            try:
                due_date = datetime.strptime(due_str, fmt).date()
                today = datetime.now().date()
                days = (due_date - today).days
                return max(0.0, days)
            except ValueError:
                continue
        return 30.0
    except:
        return 30.0

def compute_priority(load, force, necessity, value, due, params=None):
    if params is None:
        params = {
            'alpha': 1.5,
            'beta': 2.0,
            'gamma': 2.5,
            'delta': 1.5,
            'w_L': 0.4,
            'w_F': 0.8,
            'k': 5.0,
            'theta': 0.75,
            'max_days': 60
        }

    L = normalize_score(load)
    F = normalize_score(force)
    N = normalize_score(necessity)
    V = normalize_score(value)

    D = parse_due_date(due)

    # --- urgency ---
    if math.isinf(D):
        U = 1.0 * (1 + params['beta'] * N)
    else:
        D = min(D, params['max_days'])
        U = (1 / (D + 1) ** params['alpha']) * (1 + params['beta'] * N)

    # --- strategy ---
    S = N ** params['gamma'] + (1 - N) * (V ** params['delta'])

    # --- execution penalty ---
    E = math.exp(-(params['w_L'] * L + params['w_F'] * F))

    priority = U * S * E

    # --- gate ---
    G = 1 / (1 + math.exp(params['k'] * (F - params['theta'])))

    final = priority * G

    return round(final * 100, 2)  # scaled output
def extract_task_fields(line: str) -> Dict[str, str]:
    fields = {'id': '', 'title': '', 'stage': '', 'force': '', 'load': '', 
              'necessity': '', 'value': '', 'due': ''}
    
    for key in fields:
        match = re.search(rf'\[{key}::\s*(.*?)\]', line)
        if match:
            fields[key] = match.group(1).strip()
    
    if not fields['title']:
        title_match = re.search(r'-\s*\[\s*\]\s*(.+?)(?:\s+#task|\s+\[)', line)
        if title_match:
            fields['title'] = title_match.group(1).strip()
    
    return fields


def update_priority_in_line(line: str, new_priority: float) -> str:
    """Replace existing priority or add new one"""
    if '[priority::' in line:
        # Replace existing priority value
        return re.sub(r'\[priority::\s*[^]]+\]', f'[priority:: {new_priority}]', line)
    else:
        # Add new priority field at the end
        return line.rstrip() + f' [priority:: {new_priority}]'


def process_vault(vault_path: str, reset: bool = False):
    vault_path = Path(vault_path)
    if not vault_path.is_dir():
        print(f"Error: {vault_path} not found.")
        return

    task_pattern = re.compile(r'^\s*-\s*\[\s*\].*?#task', re.MULTILINE)
    
    updated_count = 0
    total_tasks = 0
    
    print(f"Scanning vault: {vault_path}")
    print(f"Mode: {'RESET (recompute all)' if reset else 'Update only missing priorities'}\n")
    
    for md_file in vault_path.rglob("*.md"):
        try:
            content = md_file.read_text(encoding='utf-8')
            original = content
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
                    fields['necessity'], fields['value'], fields['due']
                )
                
                # Update if reset or no priority exists
                if reset or '[priority::' not in task_line:
                    updated_line = update_priority_in_line(task_line, prio)
                    content = content[:start] + updated_line + content[line_end:]
                    offset += len(updated_line) - len(task_line)
                    updated_count += 1
                    
                    status = "RESET" if reset and '[priority::' in task_line else "✓ Updated"
                    print(f"{status}: {fields['title'] or 'Untitled':40} → {prio}")
                else:
                    print(f"→ Skipped (has priority): {fields['title'] or 'Untitled':40}")
            
            if content != original:
                md_file.write_text(content, encoding='utf-8')
                
        except Exception as e:
            print(f"Error in {md_file.name}: {e}")
    
    print("\n" + "="*75)
    print(f"✅ Finished! {updated_count} tasks processed out of {total_tasks} found.")
    print("="*75)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update task priorities in Obsidian vault")
    parser.add_argument("vault_path", help="Path to your Obsidian vault")
    parser.add_argument("--reset", action="store_true", help="Recompute priorities for ALL tasks (overwrite existing)")
    args = parser.parse_args()
    
    process_vault(args.vault_path, reset=args.reset)