#!/usr/bin/env python3
import re
import json
import logging
import os

# Temporarily remove global LOG_FILE and define it within main
# This is to ensure correct path resolution for logging

def get_header_info(line):
    """Extract header level and title from a line"""
    header_pattern = re.compile(r"^(#{1,6})\s*(.*?)\s*$")
    match = header_pattern.match(line.strip())
    if match:
        level = len(match.group(1))
        title_text = match.group(2).strip()
        # Only return header info if there's actual content after the # symbols
        if title_text:
            return level, title_text
        else:
            # Empty header, return level but no title
            return level, None
    return None, None

def extract_raw_titles(file_path: str) -> list:
    """
    Lee un archivo Markdown y extrae títulos con su jerarquía numérica (addr)
    y número de línea, con un sistema de numeración corregido.
    - El número siempre empieza en 1 para cada nivel de header
    - Si se encuentra un header de nivel superior (menos #), se reinician los contadores inferiores
    - Se ignoran los # que estén dentro de bloques de código
    - Se maneja el patrón donde después de un encabezado vacío sigue el título real en la siguiente línea

    Args:
        file_path (str): La ruta al archivo Markdown.

    Returns:
        list: Una lista de objetos: {addr, title, line, level}.
    """
    logging.info(f"Iniciando la extracción de títulos v5 del archivo: {file_path}")
    sections = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        logging.error(f"Error: El archivo no fue encontrado en la ruta: {file_path}")
        return []
    except Exception as e:
        logging.error(f"Ocurrió un error inesperado al leer el archivo {file_path}: {e}")
        return []

    # Contadores para cada nivel (H1, H2, H3...)
    counters = {l: 0 for l in range(1, 7)}  # Inicializar todos los contadores a 0
    last_level = 0  # Track the previous header level to handle resets properly

    # Variables para rastrear si estamos dentro de un bloque de código
    in_code_block = False
    # Variable para rastrear encabezados vacíos
    pending_empty_header = None

    for line_num, line in enumerate(lines, start=1):
        # Verificar si estamos entrando o saliendo de un bloque de código
        stripped_line = line.strip()
        if stripped_line.startswith("```"):
            in_code_block = not in_code_block
            continue  # Saltar líneas de inicio/fin de bloques de código

        # Si estamos dentro de un bloque de código, no procesar encabezados
        if in_code_block:
            continue

        # Verificar si es un encabezado vacío
        header_match = re.match(r"^(#{1,6})\s*$", stripped_line)
        if header_match:
            # Es un encabezado vacío, almacenarlo temporalmente
            empty_header_level = len(header_match.group(1))
            pending_empty_header = (empty_header_level, line_num)
            continue  # Saltar esta línea pero recordarla

        # Si hay un encabezado vacío pendiente, verificar si esta línea puede ser su título
        if pending_empty_header is not None:
            level, header_line_num = pending_empty_header
            # Check if this line is an empty line or a common markdown element to skip
            if not stripped_line or \
               stripped_line.startswith("#") or \
               stripped_line.startswith("```") or \
               stripped_line.startswith("- ") or \
               stripped_line.startswith("* ") or \
               re.fullmatch(r"\[.*?\]\(.*?\)", stripped_line) or \
               re.match(r"\[\u200b?", stripped_line) or \
               re.match(r"\]\(https?://.*\)", stripped_line): # Specific patterns for the broken links
                continue # Skip this line and continue looking for the title

            # If we reach here, this line is a strong candidate for a title.
            title_text = stripped_line.strip()

            # Handle level reset when moving to a higher level (less #)
            if level < last_level:
                for l in range(level + 1, 7):
                    counters[l] = 0
                counters[level] = 0

            counters[level] += 1
            for l in range(level + 1, 7):
                counters[l] = 0

            addr = f"{level}.{counters[level]}"

            logging.debug(f"Título encontrado (después de encabezado vacío): Nivel MD={level}, Texto='{title_text}', Addr='{addr}', Línea={line_num}")

            sections.append({
                "addr": addr,
                "title": title_text,
                "line": line_num,
                "level": level,
                "raw_md_line": lines[line_num - 1].strip() # Store the raw MD line content
            })

            last_level = level
            pending_empty_header = None # Reset after finding the title
            continue # Move to the next line

        # Procesar encabezados normales
        level, title_text = get_header_info(line)

        if level is not None and title_text is not None:  # Found a header with text
            # Handle level reset when moving to a higher level (less #)
            # If the current level is higher than the previous level (meaning we're going to a more significant heading),
            # reset the counters for deeper levels AND the current level if needed
            if level < last_level:
                # If we're going to a higher-level header (e.g., from ## to #), reset deeper levels
                for l in range(level + 1, 7):
                    counters[l] = 0
                # Also reset the current level counter to start fresh
                counters[level] = 0

            # Increment the counter for the current level
            counters[level] += 1

            # Reset counters for all deeper levels to ensure proper sequencing
            for l in range(level + 1, 7):
                counters[l] = 0

            # Build address: "Level.Position" - always start at 1 for each level after reset
            addr = f"{level}.{counters[level]}"

            logging.debug(f"Título encontrado: Nivel MD={level}, Texto='{title_text}', Addr='{addr}', Línea={line_num}")

            sections.append({
                "addr": addr,
                "title": title_text,
                "line": line_num,
                "level": level,
                "raw_md_line": lines[line_num - 1].strip() # Store the raw MD line content
            })

            last_level = level

    logging.info(f"Extracción de títulos v5 completada. Se encontraron {len(sections)} títulos.")
    return sections

def read_markdown_file_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        logging.error(f"Markdown file not found: {file_path}")
        return None
    except Exception as e:
        logging.error(f"Error reading Markdown file {file_path}: {e}")
        return None

def count_effective_content_lines(markdown_lines, start_line_idx, end_line_idx, current_title_line_idx, current_title, current_level):
    non_empty_content_lines = 0
    in_code_block_for_coherence = False

    for seg_line_idx in range(start_line_idx, end_line_idx):
        if seg_line_idx >= len(markdown_lines):
            break
        seg_line = markdown_lines[seg_line_idx]
        stripped_seg_line = seg_line.strip()

        # Skip the title line itself when counting content lines
        if seg_line_idx == current_title_line_idx:
            # If the title itself is the only thing on this line, don't count it as content.
            # If there's more after the title on the same line, that's content.
            # For simplicity, if the line contains the title, we skip it.
            # We need to be careful here if the title is actually part of a longer line of text.
            # For now, let's just skip the line if it directly contains the title text.
            if stripped_seg_line == current_title or \
               (current_level >= 1 and stripped_seg_line.startswith("#" * current_level) and stripped_seg_line[current_level:].strip() == current_title):
                continue
            elif re.match(r"^\d+\.\s", current_title) and stripped_seg_line == current_title:
                continue

        # Toggle code block state
        if stripped_seg_line.startswith("```"):
            in_code_block_for_coherence = not in_code_block_for_coherence
            continue

        if in_code_block_for_coherence:
            continue

        # Skip empty lines, markdown headers, list markers, and pure links
        if not stripped_seg_line or \
           stripped_seg_line.startswith("#") or \
           stripped_seg_line.startswith("- ") or \
           stripped_seg_line.startswith("* ") or \
           re.match(r"^\d+\.\s", stripped_seg_line) or \
           re.fullmatch(r"\[.*?\]\(.*?\)", stripped_seg_line) or \
           re.match(r"\[\u200b?", stripped_seg_line) or \
           re.match(r"\]\(https?://.*\)", stripped_seg_line):
            continue
        
        non_empty_content_lines += 1
    return non_empty_content_lines


def filter_and_refine_titles(raw_titles: list, markdown_lines: list) -> list:
    refined_titles = []
    
    # Sort raw_titles by line number to ensure correct segment calculation
    raw_titles.sort(key=lambda x: x["line"])

    for i, entry in enumerate(raw_titles):
        title = entry["title"]
        line_num_in_json = entry["line"] # 1-indexed from JSON
        level = entry["level"]
        addr = entry["addr"]

        # Find the actual line index where the title is found in markdown_lines
        # This is similar to the correctness check in verify_index.py
        actual_title_line_idx = -1
        search_range_start_idx = max(0, line_num_in_json - 1)
        search_range_end_idx = min(len(markdown_lines), line_num_in_json + 10) 

        for current_md_line_idx in range(search_range_start_idx, search_range_end_idx):
            if current_md_line_idx >= len(markdown_lines):
                break
            md_line = markdown_lines[current_md_line_idx].strip()
            
            if title == md_line or md_line.startswith(title):
                actual_title_line_idx = current_md_line_idx
                break
            expected_prefix = "#" * level
            if level >= 1 and md_line.startswith(expected_prefix) and md_line[len(expected_prefix):].strip() == title:
                actual_title_line_idx = current_md_line_idx
                break
            if re.match(r"^\d+\.\s", title) and md_line == title:
                actual_title_line_idx = current_md_line_idx
                break
        
        # If we couldn't find the title on any line (shouldn't happen if extraction is good), skip.
        if actual_title_line_idx == -1:
            logging.warning(f"Title '{title}' (line {line_num_in_json}) not found in MD lines for coherence check. Skipping.")
            continue


        # Determine the end line for content check (0-indexed)
        segment_end_idx = len(markdown_lines) # Default to end of file (0-indexed)
        if i + 1 < len(raw_titles):
            next_title_json_line = raw_titles[i+1]["line"]
            # To find the true start of the next title, we'd ideally run a similar search logic.
            # For simplicity, we'll use the JSON reported line for the next title as the end of this segment.
            segment_end_idx = next_title_json_line - 1 

        effective_content_lines = count_effective_content_lines(
            markdown_lines, 
            actual_title_line_idx, # Start counting from where the title was actually found
            segment_end_idx, 
            actual_title_line_idx, # Pass the actual title line index for skipping its own line
            title, 
            level
        )

        # Heuristic: Only keep titles that represent a "substantial section"
        # User requested "más de una línea" (more than one line), so threshold > 1.
        if effective_content_lines >= 2:
            refined_titles.append(entry)
        else:
            logging.info(f"Filtered out title '{title}' (addr={addr}, line={line_num_in_json}) due to insufficient content ({effective_content_lines} lines).")

    # Re-calculate addr after filtering, as numbering might change
    final_titles = []
    counters = {l: 0 for l in range(1, 7)}
    last_level = 0

    for entry in refined_titles:
        level = entry["level"]
        title = entry["title"]
        line = entry["line"]

        if level < last_level:
            for l in range(level + 1, 7):
                counters[l] = 0
            counters[level] = 0

        counters[level] += 1
        for l in range(level + 1, 7):
            counters[l] = 0

        new_addr = f"{level}.{counters[level]}"
        final_titles.append({
            "addr": new_addr,
            "title": title,
            "line": line,
            "level": level
        })
        last_level = level
    
    return final_titles

def save_sections_to_json(sections: list, output_file: str):
    """
    Guarda la lista de secciones en un archivo JSON con formato optimizado.
    Cada registro se muestra horizontalmente, con otros elementos verticales.

    Args:
        sections (list): La lista de diccionarios de secciones.
        output_file (str): La ruta al archivo JSON de salida.
    """
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Custom JSON formatting to put record fields on one line
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("[\n")
            for i, section in enumerate(sections):
                # Properly escape quotes and newlines in the title to ensure valid JSON
                escaped_title = section["title"].replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
                # Format each section record on a single line
                record_str = f'  {{"addr": "{section["addr"]}", "title": "{escaped_title}", "line": {section["line"]}, "level": {section["level"]}}}'
                f.write(record_str)
                if i < len(sections) - 1:
                    f.write(",")
                f.write("\n")
            f.write("]\n")

        logging.info(f"Secciones guardadas exitosamente en: {output_file}")
    except Exception as e:
        logging.error(f"Error al guardar las secciones en {output_file}: {e}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Get absolute path of script's directory

    INPUT_FILE_RELATIVE = "../documentaci'on selecta.md"
    OUTPUT_INDEX_FILE_RELATIVE = "../output/extracted_titles_index_v5.json"
    LOG_FILE_RELATIVE = "../temp/extract_titles_v5.log"

    input_file_path = os.path.join(script_dir, INPUT_FILE_RELATIVE)
    output_index_file_path = os.path.join(script_dir, OUTPUT_INDEX_FILE_RELATIVE)
    log_file_path = os.path.join(script_dir, LOG_FILE_RELATIVE)

    # Configure logging with the resolved absolute path
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s",
                        handlers=[
                            logging.FileHandler(log_file_path, mode="w"), # Use the absolute path here
                            logging.StreamHandler()
                        ])

    markdown_content_lines = read_markdown_file_content(input_file_path)
    if markdown_content_lines:
        raw_sections = extract_raw_titles(input_file_path)
        if raw_sections:
            filtered_sections = filter_and_refine_titles(raw_sections, markdown_content_lines)
            save_sections_to_json(filtered_sections, output_index_file_path)
            logging.info(f"Final output has {len(filtered_sections)} coherent titles.")
        else:
            logging.warning("No raw sections extracted.")
    else:
        logging.error("Could not read Markdown content.")
