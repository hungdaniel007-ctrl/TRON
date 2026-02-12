#!/bin/bash
# Sample Validation Script for Documentation Index
#
# This script demonstrates how to validate segments of a documentation index
# against the original document without reading the entire file.
# This approach is efficient for large documents and avoids token consumption.

set -e  # Exit immediately if a command exits with a non-zero status

ORIGINAL_DOC="Scripts de Ejemplo Documentadores/SqlAlchemyDocs.md"
INDEX_FILE="output/sqlalchemy_index.json"

echo "Validating index against original document using sampling technique..."
echo "Original document has $(wc -l < "$ORIGINAL_DOC") lines"
echo "Index contains $(jq '. | length' "$INDEX_FILE") entries"
echo ""

# Extract random entries from the index and validate them
total_entries=$(jq '. | length' "$INDEX_FILE")

# Define specific indices to sample (using fixed positions to ensure reproducible results)
sample_indices=(0 100 250 500 1000 1500 2000 2200 2300 2428)  # Last index is the max possible

# Validate each selected entry
for idx in "${sample_indices[@]}"; do
    if [ $idx -ge $total_entries ]; then
        continue  # Skip if index is out of bounds
    fi
    
    # Extract the entry from the JSON array
    entry=$(jq ".[$idx]" "$INDEX_FILE")
    
    # Parse the entry
    addr=$(echo "$entry" | jq -r '.addr')
    title=$(echo "$entry" | jq -r '.title' | sed 's/"/\\"/g')  # Escape quotes for comparison
    line=$(echo "$entry" | jq -r '.line')
    level=$(echo "$entry" | jq -r '.level')
    
    echo "Sample $idx: Addr=$addr, Line=$line, Level=$level"
    echo "Title: '$title'"
    
    # Get the corresponding line from the original document
    actual_line=$(sed -n "${line}p" "$ORIGINAL_DOC")
    
    # Extract title from the actual line based on header level
    if [[ $level -eq 1 ]]; then
        actual_title=$(echo "$actual_line" | sed 's/^#\s*//' | sed 's/\s*$//')
    elif [[ $level -eq 2 ]]; then
        actual_title=$(echo "$actual_line" | sed 's/^##\s*//' | sed 's/\s*$//')
    elif [[ $level -eq 3 ]]; then
        actual_title=$(echo "$actual_line" | sed 's/^###\s*//' | sed 's/\s*$//')
    elif [[ $level -eq 4 ]]; then
        actual_title=$(echo "$actual_line" | sed 's/^####\s*//' | sed 's/\s*$//')
    elif [[ $level -eq 5 ]]; then
        actual_title=$(echo "$actual_line" | sed 's/^#####\s*//' | sed 's/\s*$//')
    elif [[ $level -eq 6 ]]; then
        actual_title=$(echo "$actual_line" | sed 's/^######\s*//' | sed 's/\s*$//')
    else
        actual_title="$actual_line"
    fi
    
    # Compare the titles (with some tolerance for special characters)
    if [ "$title" = "$actual_title" ] || [[ "$actual_line" == *"$title"* ]]; then
        echo "✓ VALID: Title matches line $line in original document"
    else
        echo "✗ INVALID: Expected '$title', got '$actual_title' at line $line"
        echo "  Full line: $actual_line"
    fi
    echo "---"
done

echo ""
echo "Sampling validation completed. This technique allows verification of index accuracy"
echo "without reading the entire $(wc -l < "$ORIGINAL_DOC")-line document."
echo ""
echo "For production use, this sampling approach validates that line numbers in the index"
echo "correctly correspond to the appropriate titles in the original document."