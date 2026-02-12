#!/bin/bash
# Complete Documentation Indexing Workflow Demonstration
#
# This script demonstrates the complete workflow for indexing large documentation files
# and validating the index against the original document.

set -e  # Exit immediately if a command exits with a non-zero status

echo "==========================================="
echo "Documentation Indexer System - Complete Workflow"
echo "==========================================="
echo ""

echo "Step 1: Setting up virtual environment..."
./setup_venv.sh
echo ""

echo "Step 2: Extracting titles from large documentation file..."
./run_extract.sh -i "Scripts de Ejemplo Documentadores/SqlAlchemyDocs.md" -o "output/sqlalchemy_index.json" --log-file "logs/workflow_extract.log"
echo ""

echo "Step 3: Verifying the generated index..."
./run_verify.sh -m "Scripts de Ejemplo Documentadores/SqlAlchemyDocs.md" -i "output/sqlalchemy_index.json" --log-file "logs/workflow_verify.log"
echo ""

echo "Step 4: Validating index accuracy using sampling technique..."
./validate_samples.sh
echo ""

echo "==========================================="
echo "Workflow completed successfully!"
echo ""
echo "Summary:"
echo "- Original document: $(wc -l < "Scripts de Ejemplo Documentadores/SqlAlchemyDocs.md") lines"
echo "- Extracted titles: $(jq '. | length' "output/sqlalchemy_index.json") entries"
echo "- Verification: Completed without issues"
echo "- Sampling validation: Performed to confirm accuracy"
echo ""
echo "The documentation indexing system has been tested on a large document"
echo "(over 277,000 lines) and successfully extracted, verified, and validated"
echo "the hierarchical structure of the documentation."
echo "==========================================="