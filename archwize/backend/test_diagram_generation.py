import requests
import pytest
import re

BASE_URL = "http://localhost:8000"

def validate_diagram_structure(mermaid_code, checklist):
    """Validates that a Mermaid diagram contains all required elements."""
    # Check if it's a valid flowchart
    assert "graph TD" in mermaid_code, "Not a top-down graph flowchart"
    
    # Check for elements in the checklist
    for item in checklist:
        if isinstance(item, str):
            assert item in mermaid_code, f"Missing element: {item}"
        elif isinstance(item, tuple) and len(item) == 2:
            # For checking node connections (source, target)
            source, target = item
            assert re.search(f"{source}.*-->.*{target}", mermaid_code, re.DOTALL), f"Missing connection: {source} --> {target}"
    
    # Check for proper node formatting with labels
    assert re.search(r'\["[^"]+"\]', mermaid_code), "No properly formatted node labels found"
    
    # Check for decision branches if needed
    if "decision" in checklist or "validate" in checklist.lower():
        assert "|" in mermaid_code, "No decision branch paths found (missing '|' syntax)"

def test_user_registration_flowchart():
    """Test case for user registration flowchart."""
    try:
        response = requests.post(f"{BASE_URL}/generate", json={"prompt": "Create a flowchart for user registration"})
        assert response.status_code == 200, f"API returned {response.status_code}"
        
        data = response.json()
        assert "mermaid_code" in data, "No mermaid_code in response"
        
        mermaid_code = data["mermaid_code"]
        checklist = [
            "Registration", "register", "Register",  # Start context
            "Details", "detail", "information", "info",  # User details
            "Validate", "validate", "Verification", "verification", "check",  # Validation
            "Valid", "Invalid", "Success", "Error", "Fail",  # Decision outcomes
            "Complete", "Completed", "Finish", "Done", "End"  # End nodes
        ]
        
        validate_diagram_structure(mermaid_code, checklist)
        
        # Print success message
        print("\n✅ User Registration Flowchart Test Passed")
        print(f"Generated Mermaid code:\n{mermaid_code}")
        
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")

def test_ecommerce_checkout_flowchart():
    """Test case for e-commerce checkout flowchart."""
    try:
        response = requests.post(f"{BASE_URL}/generate", json={"prompt": "Create a flowchart for an e-commerce checkout process"})
        assert response.status_code == 200
        
        data = response.json()
        assert "mermaid_code" in data
        
        mermaid_code = data["mermaid_code"]
        checklist = [
            "Cart", "cart", "Checkout", "checkout",  # Cart/checkout context
            "Payment", "payment", "Card", "card", "Details",  # Payment steps
            "Order", "order", "Confirm", "confirm",  # Order confirmation
            "Valid", "Invalid", "Success", "Error", "Fail",  # Decision paths
            "Complete", "Completed", "Placed", "Finish", "Done", "End"  # End states
        ]
        
        validate_diagram_structure(mermaid_code, checklist)
        
        # Print success message
        print("\n✅ E-commerce Checkout Flowchart Test Passed")
        print(f"Generated Mermaid code:\n{mermaid_code}")
        
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")

def test_api_request_flowchart():
    """Test case for API request lifecycle flowchart."""
    try:
        response = requests.post(f"{BASE_URL}/generate", json={"prompt": "Generate a flowchart for an API request lifecycle"})
        assert response.status_code == 200
        
        data = response.json()
        assert "mermaid_code" in data
        
        mermaid_code = data["mermaid_code"]
        checklist = [
            "API", "api", "Request", "request",  # API context
            "Auth", "auth", "Authenticate", "authenticate", "token",  # Auth step
            "Process", "process", "Valid", "Invalid",  # Process and validation
            "Response", "response", "Error", "error",  # Response handling
            "Complete", "Completed", "Finish", "Done", "End"  # End states
        ]
        
        validate_diagram_structure(mermaid_code, checklist)
        
        # Print success message
        print("\n✅ API Request Lifecycle Flowchart Test Passed")
        print(f"Generated Mermaid code:\n{mermaid_code}")
        
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")

def test_login_authentication_flowchart():
    """Test case for user login and authentication flowchart."""
    try:
        response = requests.post(f"{BASE_URL}/generate", json={"prompt": "Create a flowchart for user login and authentication"})
        assert response.status_code == 200
        
        data = response.json()
        assert "mermaid_code" in data
        
        mermaid_code = data["mermaid_code"]
        checklist = [
            "Login", "login", "Credentials", "credentials", "User",  # Login context
            "Validate", "validate", "Verify", "verify", "Check", "check",  # Validation step
            "Access", "access", "Granted", "granted", "Denied", "denied",  # Access states
            "Retry", "retry", "Again", "again",  # Retry flow
            "Success", "success", "Fail", "fail", "Failed", "failed",  # Outcome states
            "Complete", "Completed", "Finish", "Done", "End"  # End states
        ]
        
        validate_diagram_structure(mermaid_code, checklist)
        
        # Print success message
        print("\n✅ Login Authentication Flowchart Test Passed")
        print(f"Generated Mermaid code:\n{mermaid_code}")
        
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")

if __name__ == "__main__":
    print("Running diagram generation tests...")
    print("Make sure the backend server is running at", BASE_URL)
    
    # Run all tests
    try:
        test_user_registration_flowchart()
        test_ecommerce_checkout_flowchart()
        test_api_request_flowchart()
        test_login_authentication_flowchart()
        
        print("\n✅ All tests passed!")
    except Exception as e:
        print(f"\n❌ Tests failed: {str(e)}") 