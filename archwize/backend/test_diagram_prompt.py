#!/usr/bin/env python
"""
Utility for manually testing diagram generation with custom prompts.
This script allows you to send custom prompts to the API and view the results.
"""

import requests
import json
import argparse
import os

def generate_diagram(prompt, server_url="http://localhost:8000"):
    """Send a prompt to the API and get the generated diagram."""
    try:
        response = requests.post(
            f"{server_url}/generate",
            json={"prompt": prompt},
            timeout=60
        )
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return False, f"Exception: {str(e)}"

def save_diagram(mermaid_code, filename):
    """Save the Mermaid diagram code to a file."""
    with open(filename, 'w') as f:
        f.write(mermaid_code)
    print(f"Diagram saved to {filename}")

def print_mermaid(mermaid_code):
    """Print the Mermaid diagram code with formatting."""
    print("\n" + "=" * 80)
    print(" GENERATED MERMAID DIAGRAM ".center(80, "="))
    print("=" * 80 + "\n")
    print(mermaid_code)
    print("\n" + "=" * 80 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Test diagram generation with custom prompts")
    parser.add_argument("prompt", nargs="?", help="The prompt to generate a diagram from")
    parser.add_argument("--server", "-s", default="http://localhost:8000", 
                      help="The server URL (default: http://localhost:8000)")
    parser.add_argument("--output", "-o", help="Save the diagram to a file")
    parser.add_argument("--interactive", "-i", action="store_true", 
                      help="Run in interactive mode, allowing multiple prompts")
    
    args = parser.parse_args()
    
    if args.interactive:
        print("Interactive Diagram Generation Mode")
        print("Type 'exit' or 'quit' to end the session\n")
        
        session_count = 1
        while True:
            prompt = input("\nEnter your diagram prompt: ")
            if prompt.lower() in ["exit", "quit"]:
                break
            
            print(f"\nGenerating diagram for prompt: '{prompt}'")
            success, result = generate_diagram(prompt, args.server)
            
            if success:
                mermaid_code = result.get("mermaid_code", "")
                print_mermaid(mermaid_code)
                
                # Offer to save the result
                save_option = input("Save this diagram? (y/n): ").lower()
                if save_option == 'y':
                    filename = input("Enter filename (or press Enter for default): ")
                    if not filename:
                        filename = f"diagram_{session_count}.md"
                    save_diagram(mermaid_code, filename)
            else:
                print(f"Failed to generate diagram: {result}")
            
            session_count += 1
    elif args.prompt:
        print(f"Generating diagram for prompt: '{args.prompt}'")
        success, result = generate_diagram(args.prompt, args.server)
        
        if success:
            mermaid_code = result.get("mermaid_code", "")
            print_mermaid(mermaid_code)
            
            if args.output:
                save_diagram(mermaid_code, args.output)
        else:
            print(f"Failed to generate diagram: {result}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 