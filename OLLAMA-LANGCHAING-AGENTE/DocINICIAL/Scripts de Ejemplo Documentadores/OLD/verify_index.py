import json
import re
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

script_dir = os.path.dirname(os.path.abspath(__file__))
MARKDOWN_FILE_PATH = os.path.join(script_dir, "../documentaci'on selecta.md")
INDEX_FILE_PATH = os.path.join(script_dir, "../output/extracted_titles_index_v5.json")

def read_markdown_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        logging.error(f"Markdown file not found: {file_path}")
        return None
    except Exception as e:
        logging.error(f"Error reading Markdown file {file_path}: {e}")
        return None

def read_json_index(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Index file not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {file_path}: {e}")
        return None
    except Exception as e:
        logging.error(f"Error reading index file {file_path}: {e}")
        return None

def verify_index_coherence_and_correctness(markdown_lines, index_data):
    issues = []
    
    if not markdown_lines:
        issues.append("Markdown content is empty or could not be read.")
        return issues
    if not index_data:
        issues.append("Index data is empty or could not be read.")
        return issues

    logging.info(f"Starting verification of {len(index_data)} titles.")

    # Sort index_data by line number to ensure correct segment calculation
    index_data.sort(key=lambda x: x["line"])

    for i, entry in enumerate(index_data):
        title = entry["title"]
        line_num_in_json = entry["line"] # 1-indexed from JSON
        level = entry["level"]
        addr = entry["addr"]

        # --- Correctness Check (Line Number & Title Match) ---
        found_title_on_line = False
        # Check a few lines around the reported line_num_in_json
        # This accounts for the empty header -> title logic where `line` points to the empty header
        # but the actual title is a few lines after.
        # Markdown lines are 0-indexed in Python, so adjust line_num_in_json
        search_range_start_idx = max(0, line_num_in_json - 1)
        # Search up to 10 lines from the reported line to find the actual title
        search_range_end_idx = min(len(markdown_lines), line_num_in_json + 10) 

        for current_md_line_idx in range(search_range_start_idx, search_range_end_idx):
            if current_md_line_idx >= len(markdown_lines):
                break
            md_line = markdown_lines[current_md_line_idx].strip()
            
            # Direct match if the title is the exact content of the line (or starts with)
            # This handles cases like "3. Dynamically Evolving Memory"
            if title == md_line or md_line.startswith(title):
                found_title_on_line = True
                break

            # Check for standard Markdown headers (e.g. # Title, ## Subtitle)
            expected_prefix = "#" * level
            # Ensure level is valid and line starts with correct prefix
            if level >= 1 and md_line.startswith(expected_prefix):
                # Check if the text after the prefix matches the title
                remaining_line = md_line[len(expected_prefix):].strip()
                if remaining_line == title:
                    found_title_on_line = True
                    break
            
            # If the title is like "1. Title", check if the Markdown line matches that pattern
            if re.match(r"^\d+\.\s", title) and md_line == title:
                found_title_on_line = True
                break

        if not found_title_on_line:
            issues.append(f"[{addr}] Correctness Issue: Title '{title}' (level {level}, JSON line {line_num_in_json}) not clearly found around original line {line_num_in_json}. Searched from line {search_range_start_idx+1} to {search_range_end_idx}.")
        
        # --- Coherence Check (Segment Length) ---
        # Content segment is from current title's actual line in MD to next title's actual line in MD
        # For this, we need the *actual* line index of the title we just found.
        # If not found, we use the JSON reported line for boundary definition for content check,
        # otherwise content_start_line_for_segment will be 0-indexed.

        # Note: current_md_line_idx from the previous loop is the *last* line searched.
        # We need the *actual* line where the title was found for the segment start.
        # If found_title_on_line is True, current_md_line_idx holds the line index where it was found.
        # If not, use the JSON line as a fallback.
        if found_title_on_line:
            segment_start_idx = current_md_line_idx
        else:
            segment_start_idx = line_num_in_json - 1 # Fallback to JSON line

        # Determine the end line for content check (0-indexed)
        segment_end_idx = len(markdown_lines) # Default to end of file (0-indexed)
        if i + 1 < len(index_data):
            next_title_json_line = index_data[i+1]["line"]
            # The next title's reported line is the upper bound for the current segment.
            # Convert to 0-indexed for slice.
            segment_end_idx = next_title_json_line - 1 

        
        non_empty_content_lines = 0
        in_code_block_for_coherence = False # Local state for this segment

        # Iterate lines within the segment
        for seg_line_idx in range(segment_start_idx, segment_end_idx):
            if seg_line_idx >= len(markdown_lines):
                break
            seg_line = markdown_lines[seg_line_idx]
            stripped_seg_line = seg_line.strip()

            # Skip the title line itself (it was already considered for correctness)
            # We want to count lines *after* the title that are actual content.
            # Only skip if this is the line we *just found* the title on for correctness check
            if seg_line_idx == segment_start_idx and found_title_on_line:
                # If the title itself is the only thing on this line, don't count it as content.
                # If there's more after the title on the same line, that's content.
                # For simplicity, if the line contains the title, we skip it.
                if stripped_seg_line == title or (level >=1 and stripped_seg_line.startswith("#" * level) and stripped_seg_line[level:].strip() == title):
                    continue


            # Toggle code block state
            if stripped_seg_line.startswith("```"):
                in_code_block_for_coherence = not in_code_block_for_coherence
                continue

            if in_code_block_for_coherence:
                continue

            # Skip empty lines, markdown headers, list markers, and pure links
            # We want to count lines of actual prose/meaningful text.
            if not stripped_seg_line or \
               stripped_seg_line.startswith("#") or \
               stripped_seg_line.startswith("- ") or \
               stripped_seg_line.startswith("* ") or \
               re.match(r"^\d+\.\s", stripped_seg_line) or \
               re.fullmatch(r"\[.*?\]\(.*?\)", stripped_seg_line) or \
               re.match(r"\[\u200b?", stripped_seg_line) or \
               re.match(r"\]\(https?://.*\)", stripped_seg_line):
                continue
            
            # If it's not a skipped element, it's content.
            non_empty_content_lines += 1

        # Heuristic threshold for "substantial section"
        # If a title has 0 non-empty content lines, it's definitely an issue.
        # If it has 1, it might still be too short. Let's flag anything < 2 for review.
        if non_empty_content_lines < 2: 
            issues.append(f"[{addr}] Coherence Issue: Title '{title}' (JSON line {line_num_in_json}) has only {non_empty_content_lines} effective content lines in its segment. It might not represent a substantial section. Segment from MD line {segment_start_idx+1} to {segment_end_idx}.")

    return issues

if __name__ == "__main__":
    markdown_content_lines = read_markdown_file(MARKDOWN_FILE_PATH)
    index_json_data = read_json_index(INDEX_FILE_PATH)

    if markdown_content_lines and index_json_data:
        all_issues = verify_index_coherence_and_correctness(markdown_content_lines, index_json_data)
        if all_issues:
            logging.warning("Verification completed with issues:")
            for issue in all_issues:
                logging.warning(issue)
        else:
            logging.info("Verification completed successfully. No coherence or correctness issues found.")
    else:
        logging.error("Could not complete verification due to missing Markdown or index file.")