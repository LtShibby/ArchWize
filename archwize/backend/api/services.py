import requests
import json
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API token from environment
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

class DiagramService:
    """Service for generating diagrams using free Hugging Face models."""
    
    @staticmethod
    async def generate_mermaid_diagram(prompt: str, orientation="TD") -> str:
        """
        Generate a Mermaid.js diagram based on a user prompt using a free Hugging Face model.
        
        Args:
            prompt (str): User's diagram description/request
            orientation (str): Diagram orientation, either "TD" (top-down) or "LR" (left-right)
            
        Returns:
            str: Mermaid.js syntax for the requested diagram
            
        Raises:
            ValueError: If diagram generation fails or produces invalid output
        """
        print(f"Generating diagram for prompt: {prompt} with orientation: {orientation}")
        
        # Using Hugging Face's free inference API with the Mistral model
        huggingface_api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        
        # Include the API token in the headers
        headers = {
            "Content-Type": "application/json"
        }
        
        # Add authorization if token is available
        if HUGGINGFACE_API_TOKEN:
            headers["Authorization"] = f"Bearer {HUGGINGFACE_API_TOKEN}"
        else:
            print("WARNING: HUGGINGFACE_API_TOKEN not found in environment variables. API calls will fail.")
            raise ValueError("Missing API token for Hugging Face. Please check your configuration.")
        
        # Adjust the orientation in the example based on user preference
        flow_direction = "TD" if orientation == "TD" else "LR"
        orientation_description = "top-down" if orientation == "TD" else "left-to-right"
        
        system_prompt = f"""
        You are an AI designed to generate **valid, properly formatted Mermaid.js diagrams** based on user descriptions.  
        
        Create a {orientation_description} flowchart ({flow_direction}) for the following:
        {prompt}
        
        Output ONLY the Mermaid.js code, nothing else.
        
        Example format:
        ```
        graph {flow_direction};
          Start["Begin Process"] --> Step1["First Step"];
          Step1 --> Decision{"Decision Point"};
          Decision -->|Yes| Step2["Second Step"];
          Decision -->|No| End["Process Complete"];
          Step2 --> End;
        ```
        
        Your diagram should have:
        - Proper node connections with arrows (-->)
        - Node text in quotes ["Text"]
        - Decision diamonds with braces {"Decision"}
        - Conditional paths marked with pipes |Condition|
        - Each line must end with semicolon except the first graph declaration
        - Use clear, meaningful labels
        """
        
        # Format the payload for Mistral
        payload = {
            "inputs": f"<s>[INST] {system_prompt} [/INST]",
            "parameters": {
                "max_new_tokens": 1024,
                "temperature": 0.5,
                "return_full_text": False
            }
        }
        
        try:
            print(f"Sending request to Hugging Face API...")
            response = requests.post(huggingface_api_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                # Extract the generated text
                result = response.json()[0]["generated_text"]
                print(f"API response successful, processing result")
                
                # Clean and format the response, preserving the orientation
                return DiagramService.clean_mermaid_code(result, orientation)
            else:
                # Log the error and raise an exception
                error_msg = f"Error from Hugging Face API: {response.status_code} - {response.text}"
                print(f"ERROR: {error_msg}")
                raise ValueError(f"Diagram generation failed: {error_msg}")
        except Exception as e:
            # Log the error and raise an exception
            error_msg = f"Error generating diagram: {str(e)}"
            print(f"ERROR: {error_msg}")
            raise ValueError(error_msg)
    
    @staticmethod
    def clean_mermaid_code(code: str, orientation="TD") -> str:
        """
        Clean and validate the generated Mermaid code.
        """
        # Extract mermaid code from response
        if "```" in code:
            # Find code between markdown code blocks
            start = code.find("```")
            end = code.rfind("```")
            if start != end:
                code = code[start+3:end].strip()
                
                # Remove language identifier if present
                if code.startswith("mermaid") or code.startswith("graph"):
                    if code.startswith("mermaid"):
                        code = code[7:].strip()
                else:
                    # If no valid syntax found, return error
                    return f"graph {orientation};\n  Start[\"Error: No valid diagram generated\"];"
        
        # Fix common syntax issues
        # 1. Ensure it starts with a graph declaration
        if not code.startswith("graph"):
            code = f"graph {orientation};\n" + code
        elif "graph" in code and not code.replace(" ", "").startswith(f"graph{orientation}"):
            # Replace the orientation
            code = re.sub(r'graph\s+[A-Z]{2}', f'graph {orientation}', code)
        
        # 2. Fix condition formatting with pipes
        code = code.replace("||", "|")
        
        # 3. Ensure all connections have a semicolon
        lines = []
        for line in code.split("\n"):
            line = line.strip()
            if line and "-->" in line and not line.endswith(";"):
                line += ";"
            if line:
                lines.append(line)
        
        code = "\n".join(lines)
        
        # 4. Replace any direct node to node connections without arrows
        # Example: "A B" should be "A --> B"
        code = re.sub(r'(\w+\["[^"]*"\])\s+(\w+\["[^"]*"\])', r'\1 --> \2', code)
        
        print(f"Cleaned Mermaid code:\n{code}")
        return code

# For testing
if __name__ == "__main__":
    import asyncio
    prompt = "Create a flowchart for user registration"
    result = asyncio.run(DiagramService.generate_mermaid_diagram(prompt))
    print(result) 