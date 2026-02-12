#!/usr/bin/env python3
import re
import json
import logging
import argparse
import sys
from pathlib import Path

class MarkdownIndustrialIndexer:
    """
    Indexador v5.6: Motor Bio-Sintáctico.
    Diferencia títulos de comentarios analizando la estructura de párrafos.
    """
    def __init__(self, input_file, output_file, log_file):
        self.input_path = Path(input_file).resolve()
        self.output_path = Path(output_file).resolve()
        self.log_path = Path(log_file).resolve()
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_logging()
        self.lines = []

    def _init_logging(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s | %(levelname)-7s | %(message)s",
            handlers=[logging.FileHandler(self.log_path, mode="w", encoding="utf-8")]
        )
        self.logger = logging.getLogger("IndexerV5.6")

    def load(self):
        if not self.input_path.exists():
            print(f"\033[1;31m[!] Error: No existe {self.input_path}\033[0m")
            return False
        with open(self.input_path, "r", encoding="utf-8") as f:
            self.lines = f.readlines()
        return True

    def is_code_pattern(self, text):
        """Detecta si un texto tiene ADN de programador."""
        patterns = [
            r" = ", r"==", r"\(.*\)", r"\[.*\]", r"assert\s", 
            r"import\s", r"from\s", r"self\.", r"\.query", r"\.scalars"
        ]
        return any(re.search(p, text) for p in patterns)

    def extract(self):
        self.logger.info("Iniciando extracción v5.6...")
        sections = []
        counters = {i: 0 for i in range(1, 7)}
        last_level = 0
        in_code_block = False

        for idx, line in enumerate(self.lines):
            # 1. Ignorar bloques ```
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block: continue

            # 2. Match de header en columna 1 (Obligatorio)
            match = re.match(r"^(#{1,6})\s+(.*)$", line)
            if not match: continue

            level = len(match.group(1))
            raw_title = match.group(2).strip()
            
            # 3. CRITERIOS DE EXCLUSIÓN (Anti-Comentarios de Código)
            # Si no tiene el ancla '¶', aplicamos filtros de sospecha
            if "¶" not in line:
                # Descartar si la línea anterior NO está vacía (los títulos reales suelen respirar)
                if idx > 0 and self.lines[idx-1].strip() != "":
                    # Excepción: Si la línea anterior es otro título, está bien
                    if not self.lines[idx-1].startswith("#"):
                        continue
                
                # Descartar si parece código puro
                if self.is_code_pattern(raw_title):
                    continue

            # Limpiar título
            clean_title = re.sub(r'\[¶\].*$', '', raw_title).strip()
            if len(clean_title) < 3: continue

            # 4. Numeración jerárquica
            if level < last_level:
                for i in range(level + 1, 7): counters[i] = 0
            counters[level] += 1
            for i in range(level + 1, 7): counters[i] = 0
            
            addr = ".".join(str(counters[l]) for l in range(1, level + 1))
            sections.append({"addr": addr, "title": clean_title, "line": idx + 1, "level": level})
            last_level = level

        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(sections, f, indent=4, ensure_ascii=False)
        
        print(f"\033[1;32m[OK] Índice generado: {len(sections)} títulos.\033[0m")
        return sections

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("-o", "--output", default="output/extracted_titles_index_v5.json")
    parser.add_argument("-l", "--log", default="temp/extract_titles_v5.log")
    args = parser.parse_args()
    idx = MarkdownIndustrialIndexer(args.input, args.output, args.log)
    if idx.load(): idx.extract()
