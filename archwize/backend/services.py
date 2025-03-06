import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DiagramService:
    """Service for generating diagrams using free Hugging Face models."""
    
    @staticmethod
    async def generate_mermaid_diagram(prompt: str) -> str:
        """
        Generate a Mermaid.js diagram based on a user prompt using a free Hugging Face model.
        
        Args:
            prompt (str): User's diagram description/request
            
        Returns:
            str: Mermaid.js syntax for the requested diagram
        """
        # Using Hugging Face's free inference API with the Mistral model
        huggingface_api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        
        # No API key needed for the free tier with limited usage
        headers = {
            "Content-Type": "application/json"
        }
        
        system_prompt = """
        You are an AI that generates valid Mermaid.js flowcharts based on user descriptions.
        Create a structured flowchart that includes:
        - A clear start node (labeled with the process beginning)
        - Process nodes (actions performed in the workflow)
        - Decision nodes (conditional branches with labeled paths)
        - End nodes (final outcomes)

        Ensure your Mermaid.js syntax is correct and logical, following proper flowchart design principles.
        
        Example of a good flowchart for user registration:
        ```mermaid
        graph TD;
          Start["User Begins Registration"] --> EnterDetails["Enter User Details"];
          EnterDetails --> Validate["Validate Input"];
          Validate -->|Valid| Success["Account Created"];
          Validate -->|Invalid| Retry["Retry Registration"];
          Retry --> EnterDetails;
          Success --> End["Registration Complete"];
        ```
        
        Always follow these guidelines:
        1. Use the graph TD; format (top-down direction)
        2. Include quotation marks for node labels
        3. Use descriptive labels for nodes and edges
        4. Add condition labels on decision branches using the | syntax
        5. Connect nodes logically based on the real-world process
        6. Include clear start and end nodes
        7. Only output valid Mermaid.js syntax
        
        Do not include any explanations or text outside the diagram code.
        """
        
        # Format the payload for Mistral
        payload = {
            "inputs": f"<s>[INST] {system_prompt}\n\nHere's the user request: {prompt} [/INST]",
            "parameters": {
                "max_new_tokens": 1024,
                "temperature": 0.5,  # Lower temperature for more structured output
                "top_p": 0.95,
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(huggingface_api_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                # Extract the generated text
                result = response.json()[0]["generated_text"]
                
                # Clean and format the response
                return await DiagramService.clean_mermaid_code(result)
            else:
                # Fallback to a simple diagram if the API is not available
                print(f"Error from Hugging Face API: {response.text}")
                return DiagramService.generate_fallback_diagram(prompt)
        except Exception as e:
            # Log the error
            print(f"Error generating diagram: {str(e)}")
            return DiagramService.generate_fallback_diagram(prompt)

    @staticmethod
    def generate_fallback_diagram(prompt: str) -> str:
        """
        Generate a more structured fallback diagram when the API is not available.
        
        Args:
            prompt (str): User's diagram description/request
            
        Returns:
            str: Simple Mermaid.js flowchart
        """
        # Extract keywords and attempt to create a more meaningful structure
        words = prompt.lower().replace(',', ' ').replace('.', ' ').split()
        
        # Common flowchart-related words
        start_words = ["begin", "start", "initiate", "create", "new"]
        process_words = ["process", "update", "generate", "calculate", "send", "receive", "check", "validate", "enter"]
        decision_words = ["if", "validate", "check", "verify", "decide", "determine", "assess", "evaluate"]
        end_words = ["end", "finish", "complete", "done", "final", "success", "conclude"]
        
        # Look for keywords in the prompt
        has_start = any(word in words for word in start_words)
        has_process = any(word in words for word in process_words)
        has_decision = any(word in words for word in decision_words)
        has_end = any(word in words for word in end_words)
        
        # Create a fallback diagram with proper structure
        diagram = "graph TD;\n"
        
        # Determine the general topic
        topic = "process"
        if "login" in prompt.lower():
            topic = "login"
        elif "register" in prompt.lower() or "registration" in prompt.lower():
            topic = "registration"
        elif "checkout" in prompt.lower() or "payment" in prompt.lower():
            topic = "checkout"
        elif "api" in prompt.lower():
            topic = "API request"
        
        # Create a structured diagram based on topic
        if topic == "login":
            diagram += '  Start["User Begins Login"] --> EnterCredentials["Enter Credentials"];\n'
            diagram += '  EnterCredentials --> ValidateCredentials["Validate Credentials"];\n'
            diagram += '  ValidateCredentials -->|Valid| Success["Login Successful"];\n'
            diagram += '  ValidateCredentials -->|Invalid| Retry["Retry Login"];\n'
            diagram += '  Retry --> EnterCredentials;\n'
            diagram += '  Success --> End["User Authenticated"];\n'
        elif topic == "registration":
            diagram += '  Start["User Begins Registration"] --> EnterDetails["Enter User Details"];\n'
            diagram += '  EnterDetails --> ValidateDetails["Validate Details"];\n'
            diagram += '  ValidateDetails -->|Valid| CreateAccount["Create Account"];\n'
            diagram += '  ValidateDetails -->|Invalid| FixDetails["Correct Details"];\n'
            diagram += '  FixDetails --> EnterDetails;\n'
            diagram += '  CreateAccount --> End["Registration Complete"];\n'
        elif topic == "checkout":
            diagram += '  Start["User Begins Checkout"] --> ReviewCart["Review Cart Items"];\n'
            diagram += '  ReviewCart --> EnterPayment["Enter Payment Details"];\n'
            diagram += '  EnterPayment --> ValidatePayment["Validate Payment"];\n'
            diagram += '  ValidatePayment -->|Valid| PlaceOrder["Place Order"];\n'
            diagram += '  ValidatePayment -->|Invalid| RetryPayment["Update Payment"];\n'
            diagram += '  RetryPayment --> EnterPayment;\n'
            diagram += '  PlaceOrder --> End["Order Complete"];\n'
        elif topic == "API request":
            diagram += '  Start["Client Sends Request"] --> ValidateRequest["Validate Request"];\n'
            diagram += '  ValidateRequest -->|Valid| ProcessRequest["Process Request"];\n'
            diagram += '  ValidateRequest -->|Invalid| RejectRequest["Reject Request"];\n'
            diagram += '  ProcessRequest --> GenerateResponse["Generate Response"];\n'
            diagram += '  GenerateResponse --> End["Send Response to Client"];\n'
            diagram += '  RejectRequest --> EndError["Return Error Response"];\n'
        else:
            # Generic process fallback
            diagram += '  Start["Begin Process"] --> Input["Process Input"];\n'
            diagram += '  Input --> Validate["Validate Input"];\n'
            diagram += '  Validate -->|Valid| Process["Process Data"];\n'
            diagram += '  Validate -->|Invalid| Retry["Retry Input"];\n'
            diagram += '  Retry --> Input;\n'
            diagram += '  Process --> Output["Generate Output"];\n'
            diagram += '  Output --> End["Process Complete"];\n'
            
        return diagram

    @staticmethod
    async def clean_mermaid_code(code: str) -> str:
        """
        Clean and validate the generated Mermaid code.
        
        Args:
            code (str): Raw Mermaid.js code
            
        Returns:
            str: Cleaned Mermaid.js code
        """
        # Remove markdown code blocks if present
        if "```mermaid" in code:
            code = code.split("```mermaid", 1)[1]
            if "```" in code:
                code = code.split("```", 1)[0]
        elif "```" in code:
            parts = code.split("```", 2)
            if len(parts) >= 3:
                code = parts[1]
                if code.startswith("mermaid\n"):
                    code = code[8:]  # Remove "mermaid\n" prefix
        
        # Ensure the code contains basic mermaid syntax
        if not any(keyword in code for keyword in ["graph ", "sequenceDiagram", "classDiagram", "erDiagram", "stateDiagram", "gantt", "pie"]):
            # If no valid syntax is found, return a generic flowchart
            return "graph TD;\n" + \
                   "  Start[\"Begin Process\"] --> Process[\"Process Data\"];\n" + \
                   "  Process --> Decision{\"Validation Check\"};\n" + \
                   "  Decision -->|Valid| Success[\"Success\"];\n" + \
                   "  Decision -->|Invalid| Retry[\"Retry\"];\n" + \
                   "  Retry --> Process;\n" + \
                   "  Success --> End[\"Process Complete\"];"
        
        # Ensure the code has graph TD; if it's a flowchart but missing this
        if "graph " not in code and any(node_marker in code for node_marker in ["-->", "==>", "-.->", "==>"]):
            code = "graph TD;\n" + code
            
        # Ensure flow direction is set to TD if not specified
        if "graph " in code and not any(direction in code for direction in ["graph TD", "graph LR", "graph RL", "graph BT"]):
            code = code.replace("graph ", "graph TD ")
        
        # Try to fix common syntax errors
        # Ensure node labels use square brackets when missing
        code_lines = code.split('\n')
        fixed_lines = []
        
        for line in code_lines:
            if "-->" in line:
                parts = line.split("-->")
                if len(parts) == 2:
                    node1 = parts[0].strip()
                    node2 = parts[1].strip()
                    
                    # Check if node1 is missing brackets
                    if node1 and not any(c in node1 for c in ['[', '(', '{', '"']):
                        node1 = f'{node1}["{node1}"]'
                    
                    # Check if node2 is missing brackets and isn't a conditional path
                    if node2 and not any(c in node2 for c in ['[', '(', '{', '"', '|']):
                        node2 = f'{node2}["{node2}"]'
                    
                    line = f"  {node1} --> {node2}"
            
            fixed_lines.append(line)
        
        code = '\n'.join(fixed_lines)
            
        return code.strip() 