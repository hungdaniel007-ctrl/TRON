#!/usr/bin/env python3
"""
Test script for running all agent tests.
This script executes various test cases for different agents and generates a summary report.
"""

import subprocess
import os
import re
import datetime
from pathlib import Path


# Define project paths
PROJECT_ROOT = Path(__file__).parent.parent  # Parent directory of TESTs
VENV_PYTHON = PROJECT_ROOT / '.venv/bin/python'
RUN_SCRIPT = PROJECT_ROOT / 'run.py'


def main():
    """Main function to run all test cases."""
    
    # Define test cases
    test_cases = [
        {
            'name': 'tron-ceo-deepseek-headless-simple',
            'agent': 'tron-ceo',
            'args': ['--agent', 'tron-ceo', '-m', 'Hello, how are you?', '--headless'],
            'check_output_regex': r'(?s)(?=.*Cargando cerebro: DeepSeek \(API\))(?!.*Error Fatal)',
            'check_stderr_for_errors': False
        },
        {
            'name': 'tron-ceo-deepseek-headless-streaming',
            'agent': 'tron-ceo',
            'args': ['--agent', 'tron-ceo', '-m', 'Stream this message', '--headless', '--stream'],
            'check_output_regex': r'(?s)(?=.*Cargando cerebro: DeepSeek \(API\))(?!.*Error Fatal)',
            'check_stderr_for_errors': False
        },
        {
            'name': 'gema-analyst-gemma-headless-simple',
            'agent': 'gema-analyst',
            'args': ['--agent', 'gema-analyst', '-m', 'Analyze this data', '--headless'],
            'check_output_regex': r'(?s)(?=.*Cargando cerebro: Gemma \(Ollama\))(?!.*Error Fatal)',
            'check_stderr_for_errors': False
        },
        {
            'name': 'gema-analyst-gemma-headless-streaming',
            'agent': 'gema-analyst',
            'args': ['--agent', 'gema-analyst', '-m', 'Provide streaming analysis', '--headless', '--stream'],
            'check_output_regex': r'(?s)(?=.*Cargando cerebro: Gemma \(Ollama\))(?!.*Error Fatal)',
            'check_stderr_for_errors': False
        },
        {
            'name': 'headless-session-persistence',
            'agent': 'tron-ceo',
            'args': ['--agent', 'tron-ceo', '-m', 'Test session persistence', '--headless', '--session', 'test_session'],
            'check_output_regex': r'(?s)(?=.*Cargando cerebro: DeepSeek \(API\))(?!.*Error Fatal)',
            'check_stderr_for_errors': False
        },
        {
            'name': 'headless-system-prompt-override',
            'agent': 'gema-analyst',
            'args': ['--agent', 'gema-analyst', '-m', 'Test system prompt', '--headless', '-ps', 'Custom system prompt'],
            'check_output_regex': r'(?s)(?=.*Cargando cerebro: Gemma \(Ollama\))(?!.*Error Fatal)',
            'check_stderr_for_errors': False
        },
    ]
    
    # Initialize results
    results = []
    
    # Iterate through each test case
    for test_case in test_cases:
        print(f"Running test: {test_case['name']}")
        
        # Construct command
        cmd = [str(VENV_PYTHON), str(RUN_SCRIPT)] + test_case['args']
        
        # Execute command
        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300,  # 5 minute timeout
            encoding="utf-8",
            errors="ignore"
        )
        
        # Create log directory for agent
        log_dir = Path(PROJECT_ROOT) / 'TESTs' / 'logs' / test_case['agent']
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Save stdout and stderr to log file
        log_file_path = log_dir / f"{test_case['name']}.log"
        with open(log_file_path, 'w', encoding='utf-8') as log_file:
            log_file.write(f"Test: {test_case['name']}\n")
            log_file.write(f"Command: {' '.join(cmd)}\n")
            log_file.write(f"Return code: {result.returncode}\n")
            log_file.write(f"Timestamp: {datetime.datetime.now()}\n")
            log_file.write("\nSTDOUT:\n")
            log_file.write(result.stdout)
            log_file.write("\nSTDERR:\n")
            log_file.write(result.stderr)
        
        # Analyze output - start with return code check
        status = 'PASS' if result.returncode == 0 else 'FAIL'

        # Check regex if specified
        if test_case.get('check_output_regex'):
            if not re.search(test_case['check_output_regex'], result.stdout, re.IGNORECASE):
                status = 'FAIL'

        # Check stderr for errors if specified
        if test_case.get('check_stderr_for_errors') and result.stderr.strip():
            if re.search(r'(error|exception|traceback)', result.stderr, re.IGNORECASE):
                status = 'FAIL'
        
        # Append result
        results.append({
            'name': test_case['name'],
            'status': status,
            'log_file': str(log_file_path),
            'return_code': result.returncode
        })
    
    # Generate summary report
    summary_path = Path(PROJECT_ROOT) / 'TESTs' / 'summary_report.txt'
    with open(summary_path, 'w', encoding='utf-8') as summary_file:
        summary_file.write(f"Test Summary Report - {datetime.datetime.now()}\n")
        summary_file.write("=" * 50 + "\n\n")
        
        for result in results:
            summary_file.write(f"Test: {result['name']}\n")
            summary_file.write(f"Status: {result['status']}\n")
            summary_file.write(f"Log File: {result['log_file']}\n")
            summary_file.write(f"Return Code: {result['return_code']}\n")
            summary_file.write("-" * 30 + "\n")
    
    # Print summary
    passed_count = sum(1 for r in results if r['status'] == 'PASS')
    total_count = len(results)
    print(f"\nTest Summary: {passed_count}/{total_count} tests passed")
    
    # Print detailed results
    for result in results:
        print(f"{result['status']}: {result['name']} - Log: {result['log_file']}")


if __name__ == '__main__':
    main()