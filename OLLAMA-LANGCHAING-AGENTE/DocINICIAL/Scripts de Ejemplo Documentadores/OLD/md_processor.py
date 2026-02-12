#!/usr/bin/env python3
import re
import json
import logging
import argparse
import os
import sys

class MarkdownProcessor:
    """Encapsula la lógica de indexación y verificación de coherencia."""
    
    def __init__(self, input_path, output_path, log_path):
        self.input_path = input_path
        self.output_path = output_path
        self.setup_logging(log_path)
        self.lines = []
        self.sections = []

    def setup_logging(self, log_path):
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s",
            handlers=[
                logging.FileHandler(log_path, mode="w"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def load_file(self):
        try:
            with open(self.input_path, "r", encoding="utf-8") as f:
                self.lines = f.readlines()
            self.logger.info(f"Archivo cargado: {self.input_path} ({len(self.lines)} líneas)")
            return True
        except Exception as e:
            self.logger.error(f"Error cargando archivo: {e}")
            return False

    def _is_code_block(self, line, state):
        if line.strip().startswith("```"):
            return not state
        return state

    def extract_raw_titles(self):
        """Extrae títulos considerando jerarquía y saltos de línea."""
        raw_sections = []
        counters = {i: 0 for i in range(1, 7)}
        last_level = 0
        in_code = False
        
        header_pattern = re.compile(r"^(#{1,6})\s*(.*)")

        for idx, line in enumerate(self.lines):
            in_code = self._is_code_block(line, in_code)
            if in_code: continue

            match = header_pattern.match(line.strip())
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()
                line_num = idx + 1

                # Si el título está vacío en la línea del #, buscar en la siguiente
                if not title and line_num < len(self.lines):
                    title = self.lines[idx + 1].strip()
                
                if not title: continue

                # Reinicio de contadores jerárquicos
                if level < last_level:
                    for i in range(level + 1, 7): counters[i] = 0
                
                counters[level] += 1
                for i in range(level + 1, 7): counters[i] = 0
                
                addr = f"{level}.{counters[level]}"
                raw_sections.append({
                    "addr": addr,
                    "title": title,
                    "line": line_num,
                    "level": level
                })
                last_level = level
        
        self.logger.debug(f"Títulos brutos encontrados: {len(raw_sections)}")
        return raw_sections

    def filter_substantial_content(self, raw_sections):
        """Filtra secciones que no tienen contenido real (mínimo 2 líneas de prosa)."""
        refined = []
        for i, section in enumerate(raw_sections):
            start_idx = section["line"] # 1-based
            end_idx = raw_sections[i+1]["line"] - 1 if i+1 < len(raw_sections) else len(self.lines)
            
            content_count = 0
            in_code = False
            for j in range(start_idx, end_idx):
                line = self.lines[j].strip()
                in_code = self._is_code_block(line, in_code)
                
                if not line or in_code or line.startswith("#") or line.startswith("```"):
                    continue
                content_count += 1
            
            if content_count >= 2:
                refined.append(section)
            else:
                self.logger.warning(f"Sección descartada por poco contenido ({content_count} líneas): {section['title']}")

        # Re-indexar tras el filtrado
        return self._recalculate_addresses(refined)

    def _recalculate_addresses(self, sections):
        final = []
        counters = {i: 0 for i in range(1, 7)}
        last_level = 0
        for s in sections:
            lvl = s["level"]
            if lvl < last_level:
                for i in range(lvl + 1, 7): counters[i] = 0
            counters[lvl] += 1
            for i in range(lvl + 1, 7): counters[i] = 0
            s["addr"] = f"{lvl}.{counters[lvl]}"
            final.append(s)
            last_level = lvl
        return final

    def save_index(self, sections):
        try:
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            with open(self.output_path, "w", encoding="utf-8") as f:
                json.dump(sections, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Índice guardado en: {self.output_path}")
        except Exception as e:
            self.logger.error(f"Error guardando JSON: {e}")

def main():
    parser = argparse.ArgumentParser(description="Indexador de Markdown Profesional")
    parser.add_argument("-i", "--input", required=True, help="Archivo Markdown de entrada")
    parser.add_argument("-o", "--output", default="output/index.json", help="Ruta del JSON de salida")
    parser.add_argument("-l", "--log", default="temp/process.log", help="Ruta del log")
    
    args = parser.parse_args()

    processor = MarkdownProcessor(args.input, args.output, args.log)
    if not processor.load_file():
        sys.exit(1)

    raw = processor.extract_raw_titles()
    filtered = processor.filter_substantial_content(raw)
    processor.save_index(filtered)
    print(f"Proceso completado. {len(filtered)} secciones indexadas.")

if __name__ == "__main__":
    main()
