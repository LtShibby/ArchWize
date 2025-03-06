// Next.js API route handler for diagram generation
// This connects to our FastAPI backend for processing

import axios from 'axios';

export default async function handler(req, res) {
  // Only accept POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ detail: 'Method not allowed' });
  }

  try {
    const { prompt } = req.body;
    
    if (!prompt) {
      return res.status(400).json({ detail: 'Prompt is required' });
    }

    // Send request to FastAPI backend
    // Replace this URL with your actual backend URL in production
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
    const response = await axios.post(`${backendUrl}/generate`, { prompt });

    // Return the mermaid code from the backend
    return res.status(200).json({ mermaid_code: response.data.mermaid_code });
  } catch (error) {
    console.error('Error generating diagram:', error);
    
    // Handle different types of errors
    if (error.response) {
      // The backend returned an error response
      return res.status(error.response.status).json({ 
        detail: error.response.data.detail || 'Backend error' 
      });
    } else if (error.request) {
      // The request was made but no response was received
      return res.status(503).json({ 
        detail: 'Could not connect to diagram generation service' 
      });
    } else {
      // Something happened in setting up the request
      return res.status(500).json({ 
        detail: 'Internal server error' 
      });
    }
  }
} 