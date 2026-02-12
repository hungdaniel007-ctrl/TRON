#!/usr/bin/env python3
import re
import json
import logging
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Optional

class MarkdownIndexer:
    """
    Indexer profesional de Markdown con soporte para jerarquías complejas,
    detección de bloques de código y validación de contenido sustancial.
    """
    def __init__(self, input_file: str, output_file: str, log_file: str):
        self.input_path = Path(input_file).resolve()
        self.output_path = Path(output_file).resolve()
        self.log_path = Path(log_file).resolve()
        
        # Garantizar infraestructura de directorios
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._setup_logging()
        self.lines: List[str] = []

    def _setup_logging(self):
        log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        logging.basicConfig(
            level=logging.DEBUG,
            format=log_format,
            handlers=[
                logging.FileHandler(self.log_path, mode="w", encoding="utf-8"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger("MD-Indexer")
        self.logger.info("Sistema de indexación inicializado.")

    def load_content(self) -> bool:
        try:
            if not self.input_path.exists():
                self.logger.error(f"Archivo no encontrado: {self.input_path}")
                return False
            with open(self.input_path, "r", encoding="utf-8") as f:
                self.lines = f.readlines()
            self.logger.info(f"Cargadas {len(self.lines)} líneas de {self.input_path.name}")
            return True
        except Exception as e:
            self.logger.critical(f"Fallo catastrófico al leer archivo: {e}", exc_info=True)
            return False

    def _is_header(self, line: str) -> Optional[tuple]:
        """Retorna (nivel, texto) si es un header, sino None."""
        match = re.match(r"^(#{1,6})\s+(.*)$", line.strip())
        if match:
            return len(match.group(1)), match.group(2).strip()
        # Caso especial: Header vacío '#'
        empty_match = re.match(r"^(#{1,6})\s*$", line.strip())
        if empty_match:
            return len(empty_match.group(1)), ""
        return None

    def process(self) -> List[Dict]:
        self.logger.info("Iniciando extracción de títulos...")
        raw_sections = []
        counters = {i: 0 for i in range(1, 7)}
        last_level = 0
        in_code_block = False

        for i, line in enumerate(self.lines):
            # Ignorar bloques de código
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue

            header_info = self._is_header(line)
            if header_info:
                level, title = header_info
                line_num = i + 1

                # Si el título está en la línea siguiente (header vacío)
                if not title and line_num < len(self.lines):
                    title = self.lines[i + 1].strip()
                
                if not title: continue

                # Lógica de numeración jerárquica
                if level < last_level:
                    for l in range(level + 1, 7): counters[l] = 0
                
                counters[level] += 1
                for l in range(level + 1, 7):
                    if l > level: counters[l] = 0
                
                addr = ".".join(str(counters[l]) for l in range(1, level + 1))
                
                raw_sections.append({
                    "addr": addr,
                    "title": title,
                    "line": line_num,
                    "level": level
                })
                last_level = level
                self.logger.debug(f"Detectado: [{addr}] {title} (Línea {line_num})")

        return self._filter_and_save(raw_sections)

    def _filter_and_save(self, sections: List[Dict]) -> List[Dict]:
        """Filtra secciones con poco contenido y guarda el JSON."""
        refined = []
        for i, sec in enumerate(sections):
            start = sec["line"]
            end = sections[i+1]["line"] - 1 if i+1 < len(sections) else len(self.lines)
            
            # Contar líneas de contenido real
            content_lines = 0
            for j in range(start, end):
                l = self.lines[j].strip()
                if l and not l.startswith("#") and not l.startswith("```"):
                    content_lines += 1
            
            if content_lines >= 2:
                refined.append(sec)
            else:
                self.logger.warning(f"Sección '{sec['title']}' descartada: contenido insuficiente ({content_lines} líneas).")

        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(refined, f, indent=4, ensure_ascii=False)
        
        self.logger.info(f"Proceso finalizado. {len(refined)} secciones guardadas en {self.output_path}")
        return refined

def main():
    parser = argparse.ArgumentParser(description="TRON MD-Indexer v6.0 - High Performance")
    parser.add_argument("-i", "--input", required=True, help="Markdown de entrada")
    parser.add_argument("-o", "--output", required=True, help="JSON de salida")
    parser.add_argument("-l", "--log", required=True, help="Archivo de log")
    args = parser.parse_args()

    indexer = MarkdownIndexer(args.input, args.output, args.log)
    if indexer.load_content():
        indexer.process()
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
