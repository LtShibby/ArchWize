#!/usr/bin/env python
"""
Test runner for ArchWize diagram generation.
This script runs the tests and provides a clear report of the results.
"""

import os
import sys
import subprocess
import requests
import json
import time
from datetime import datetime

def print_header(text):
    """Print a formatted header."""
    terminal_width = 80
    print("\n" + "=" * terminal_width)
    print(f" {text} ".center(terminal_width, "="))
    print("=" * terminal_width + "\n")

def check_server_running():
    """Check if the backend server is running."""
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            return True
    except:
        return False
    return False

def run_test_command():
    """Run the test file as a module."""
    result = subprocess.run([sys.executable, "test_diagram_generation.py"], 
                          capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def sample_test_requests():
    """Generate sample test requests to validate diagram generation."""
    test_requests = [
        "Create a flowchart for user registration",
        "Create a flowchart for an e-commerce checkout process", 
        "Generate a flowchart for an API request lifecycle",
        "Create a flowchart for user login and authentication"
    ]
    
    results = []
    
    for prompt in test_requests:
        print(f"Testing: {prompt}")
        try:
            response = requests.post("http://localhost:8000/generate", 
                                   json={"prompt": prompt}, timeout=30)
            if response.status_code == 200:
                mermaid_code = response.json().get("mermaid_code", "")
                
                # Basic validation
                is_valid = "graph TD" in mermaid_code and "-->" in mermaid_code
                
                results.append({
                    "prompt": prompt,
                    "success": True,
                    "status_code": response.status_code,
                    "is_valid": is_valid,
                    "mermaid_code": mermaid_code
                })
                print(f"✅ Success - Valid: {is_valid}")
            else:
                results.append({
                    "prompt": prompt,
                    "success": False,
                    "status_code": response.status_code,
                    "error": response.text
                })
                print(f"❌ Failed - Status code: {response.status_code}")
        except Exception as e:
            results.append({
                "prompt": prompt,
                "success": False,
                "error": str(e)
            })
            print(f"❌ Failed - Error: {str(e)}")
            
    return results

def save_test_results(results):
    """Save test results to a file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_results_{timestamp}.json"
    
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nTest results saved to {filename}")

def main():
    """Main test runner function."""
    print_header("ArchWize Diagram Generation Test Runner")
    
    print("Checking if backend server is running...")
    if not check_server_running():
        print("❌ Backend server is not running. Please start it first:")
        print("   uvicorn main:app --reload")
        return 1
    
    print("✅ Backend server is running")
    
    # Run the test module
    print_header("Running Test Suite")
    exit_code, stdout, stderr = run_test_command()
    
    if stdout:
        print(stdout)
    if stderr:
        print("ERRORS:")
        print(stderr)
    
    if exit_code != 0:
        print(f"❌ Tests failed with exit code {exit_code}")
    else:
        print("✅ All tests passed!")
    
    # Generate sample test requests
    print_header("Generating Sample Test Diagrams")
    print("This may take a minute as we test multiple prompts...")
    results = sample_test_requests()
    
    # Analyze results
    success_count = sum(1 for r in results if r.get("success", False))
    valid_count = sum(1 for r in results if r.get("is_valid", False))
    
    print(f"\nResults: {success_count}/{len(results)} successful API calls")
    print(f"         {valid_count}/{len(results)} valid Mermaid diagrams")
    
    # Save results
    save_test_results(results)
    
    return 0 if exit_code == 0 and success_count == len(results) else 1

if __name__ == "__main__":
    sys.exit(main()) 