#!/usr/bin/env python3
"""
Generate JSON audit report for pokemon-dev workspace
"""
import subprocess
import json
from datetime import datetime

def get_dir_size(path):
    """Get directory size using du"""
    result = subprocess.run(['du', '-sh', path], capture_output=True, text=True)
    if result.returncode == 0:
        size = result.stdout.split()[0]
        return size
    return "0"

def get_file_count(pattern, exclude=None):
    """Count files matching pattern"""
    if '*' in pattern:
        # Handle wildcards
        if pattern == '*.ts':
            cmd = ['find', '.', '-name', '*.ts', '-o', '-name', '*.tsx']
        else:
            cmd = ['find', '.', '-name', pattern]
    else:
        cmd = ['find', '.', '-type', pattern]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    files = [f for f in result.stdout.split('\n') if f]
    if exclude:
        files = [f for f in files if exclude not in f]
    return len(files)

def get_top_level_dirs():
    """Get top-level directories with sizes"""
    result = subprocess.run(['du', '-sh', '*/'], capture_output=True, text=True, shell=False)
    dirs = []
    for line in result.stdout.strip().split('\n'):
        if line:
            # du outputs: SIZE\tPATH or SIZE PATH
            line = line.strip()
            # Try tab first, then space
            if '\t' in line:
                parts = line.split('\t', 1)
            else:
                parts = line.split(None, 1)
            
            if len(parts) >= 2:
                size = parts[0]
                name = parts[1].rstrip('/')
                dirs.append({"name": name, "size": size})
    return sorted(dirs, key=lambda x: parse_size(x['size']), reverse=True)

def parse_size(size_str):
    """Parse size string to bytes for sorting"""
    multipliers = {'K': 1024, 'M': 1024*1024, 'G': 1024*1024*1024}
    if size_str[-1] in multipliers:
        num = float(size_str[:-1])
        return num * multipliers[size_str[-1]]
    return float(size_str)

def get_frontend_versions():
    """Get frontend version sizes"""
    result = subprocess.run(['du', '-sh', 'frontends/*/'], capture_output=True, text=True, cwd='.')
    versions = []
    for line in result.stdout.strip().split('\n'):
        if line:
            parts = line.split('\t')
            if len(parts) >= 2:
                size = parts[0]
                path = parts[1]
            else:
                parts = line.split()
                if len(parts) >= 2:
                    size = parts[0]
                    path = ' '.join(parts[1:])
                else:
                    continue
            port = path.split('/')[-1].replace('port-', '').rstrip('/')
            versions.append({"port": port, "size": size})
    return sorted(versions, key=lambda x: parse_size(x['size']), reverse=True)

def main():
    audit = {
        "generated": datetime.now().isoformat(),
        "totalSize": get_dir_size('.'),
        "totalFiles": get_file_count('f'),
        "totalDirectories": get_file_count('d'),
        "topLevelDirectories": get_top_level_dirs(),
        "frontendVersions": get_frontend_versions(),
        "fileTypes": {
            "typescript": get_file_count('*.ts', exclude='node_modules') + get_file_count('*.tsx', exclude='node_modules'),
            "python": get_file_count('*.py', exclude='node_modules'),
            "markdown": get_file_count('*.md', exclude='node_modules'),
            "javascript": get_file_count('*.js', exclude='node_modules'),
            "css": get_file_count('*.css', exclude='node_modules')
        }
    }
    
    print(json.dumps(audit, indent=2))

if __name__ == '__main__':
    main()
