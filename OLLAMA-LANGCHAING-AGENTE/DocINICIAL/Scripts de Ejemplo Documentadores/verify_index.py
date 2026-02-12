#!/usr/bin/env python3
import json
import argparse
from pathlib import Path

# Paleta Guacamaya
C = {
    1: "\033[1;31m", 2: "\033[1;33m", 3: "\033[1;32m",
    4: "\033[1;36m", 5: "\033[1;34m", 6: "\033[1;35m",
    "ERR": "\033[41;37m", "OK": "\033[1;32m", "LINE": "\033[1;32m",
    "CTX": "\033[90m", "RESET": "\033[0m", "DIV": "\033[1;30m"
}

def print_context(lines, target_idx, ctx_range):
    start = max(0, target_idx - ctx_range)
    end = min(len(lines), target_idx + ctx_range + 1)
    for i in range(start, end):
        # Números limpios, sin puntos
        num = f"{i+1:6}"
        if i == target_idx:
            print(f"{C['LINE']}{num} -> {lines[i].rstrip()}{C['RESET']}")
        else:
            print(f"{C['CTX']}{num}    {lines[i].rstrip()}{C['RESET']}")

def verify(md_path, json_path, solo_errores, nivel_max, contexto):
    md_path, json_path = Path(md_path), Path(json_path)
    if not md_path.exists() or not json_path.exists(): return
    
    with open(md_path, "r", encoding="utf-8") as f: lines = f.readlines()
    with open(json_path, "r", encoding="utf-8") as f: index = json.load(f)

    errors = 0
    for entry in index:
        lvl = entry["level"]
        if nivel_max and lvl > nivel_max: continue
        
        line_idx = entry["line"] - 1
        expected = entry["title"]
        actual_line = lines[line_idx].strip() if line_idx < len(lines) else "EOF"
        
        success = expected in actual_line
        if solo_errores and success: continue
        
        status = f"{C['OK']}[OK]{C['RESET']}" if success else f"{C['ERR']}[FALLO]{C['RESET']}"
        c_lvl = C.get(lvl, C['RESET'])
        
        print(f"{status} {c_lvl}Lvl {lvl}{C['RESET']} | {C['CTX']}Addr {entry['addr']:12}{C['RESET']} | {expected}")
        
        if contexto > 0 or not success:
            print_context(lines, line_idx, contexto)
            print(f"{C['DIV']}----------------------------------------{C['RESET']}")
        
        if not success: errors += 1

    print(f"\n{C[2]}Auditados: {len(index)} | Errores: {errors}{C['RESET']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown")
    parser.add_argument("json")
    parser.add_argument("-SoloErrores", type=int, default=0)
    parser.add_argument("-Nivel", type=int, default=0)
    parser.add_argument("-Contexto", type=int, default=0)
    args = parser.parse_args()
    verify(args.markdown, args.json, args.SoloErrores, args.Nivel, args.Contexto)
