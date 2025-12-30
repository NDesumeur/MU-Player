import re
import os

def remove_comments(code):
    lines = code.split('\n')
    result = []
    
    for line in lines:
        stripped = line.strip()
        
        if not stripped or stripped.startswith('#'):
            if not stripped:
                result.append('')
            continue
        
        if '#' in line:
            in_single = False
            in_double = False
            for i, char in enumerate(line):
                if char == "'" and (i == 0 or line[i-1] != '\\'):
                    in_single = not in_single
                elif char == '"' and (i == 0 or line[i-1] != '\\'):
                    in_double = not in_double
                elif char == '#' and not in_single and not in_double:
                    line = line[:i].rstrip()
                    break
        
        result.append(line)
    
    final_result = []
    empty_count = 0
    for line in result:
        if line.strip() == '':
            empty_count += 1
            if empty_count <= 2:
                final_result.append(line)
        else:
            empty_count = 0
            final_result.append(line)
    
    return '\n'.join(final_result)

files_to_clean = ['main.py', 'MU Player.py']

for file in files_to_clean:
    if os.path.exists(file):
        print(f"Cleaning {file}...")
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        cleaned = remove_comments(content)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        print(f"[OK] {file} cleaned")

print("All files cleaned!")
