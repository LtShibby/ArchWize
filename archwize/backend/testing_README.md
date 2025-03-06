# ArchWize Diagram Generation Testing Tools

This directory contains tools for testing the diagram generation capabilities of ArchWize.

## Available Testing Tools

### 1. Automated Test Suite (`test_diagram_generation.py`)

This file contains automated tests that verify the diagram generation functionality meets the requirements for various use cases.

The tests check that generated diagrams:
- Have proper structure (start, process, decision, end nodes)
- Include necessary components for the specific workflow
- Use correct Mermaid.js syntax

### 2. Test Runner (`run_tests.py`)

A script that runs all tests and generates a test report.

**Usage:**
```bash
python run_tests.py
```

**Features:**
- Checks if the backend server is running
- Runs the automated test suite
- Generates sample test diagrams
- Provides a summary of test results
- Saves results to a JSON file for later analysis

### 3. Manual Testing Tool (`test_diagram_prompt.py`)

A utility for manually testing diagram generation with custom prompts.

**Usage:**
```bash
# Simple usage with a prompt
python test_diagram_prompt.py "Create a flowchart for user registration"

# Save the diagram to a file
python test_diagram_prompt.py "Create a flowchart for user login" --output login_diagram.md

# Interactive mode
python test_diagram_prompt.py --interactive
```

**Features:**
- Test custom prompts interactively
- View the generated Mermaid.js code
- Save diagrams to files
- Supports multiple diagrams in a single session

## Testing Checklist

When testing diagram generation, check that the diagrams:

✅ Include a clear start node
✅ Have proper process nodes (actions)
✅ Contain decision nodes with conditional paths
✅ End with appropriate end nodes
✅ Follow logical flow based on the real-world process
✅ Use correct Mermaid.js syntax

## Sample Test Cases

1. **User Registration Flow**
   - Input: "Create a flowchart for user registration"
   - Expected: Diagram with user details entry, validation, success/failure paths

2. **E-Commerce Checkout Process**
   - Input: "Create a flowchart for an e-commerce checkout process"
   - Expected: Diagram with cart review, payment, validation, order confirmation

3. **API Request Lifecycle**
   - Input: "Generate a flowchart for an API request lifecycle"
   - Expected: Diagram with request receipt, authentication, processing, response generation

4. **Login Authentication Process**
   - Input: "Create a flowchart for user login and authentication"
   - Expected: Diagram with credential entry, validation, access control, retry mechanism

## Requirements

- Python 3.8+
- Requests library
- Running ArchWize backend server 