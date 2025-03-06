// Next.js API route handler for diagram generation
// This connects to our FastAPI backend for processing

import axios from 'axios';

export default async function handler(req, res) {
  // Only accept POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, error: 'method_not_allowed', message: 'Method not allowed' });
  }

  try {
    const { prompt, orientation = 'TD' } = req.body;
    
    if (!prompt) {
      return res.status(400).json({ success: false, error: 'missing_prompt', message: 'Prompt is required' });
    }

    // Determine the API URL based on environment
    const isProduction = process.env.NODE_ENV === 'production';
    
    // In production, use the API route in the same Vercel deployment
    // In development, use the local backend server
    const apiUrl = isProduction 
      ? '/api/generate'
      : 'http://localhost:8000/generate';
    
    console.log(`Using API URL: ${apiUrl}`);
    
    // Send request to backend
    const response = await axios.post(apiUrl, { 
      prompt,
      orientation
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });

    // Extract diagram data from response
    if (response.data && response.data.success === false) {
      return res.status(400).json({
        success: false,
        error: response.data.error || 'backend_error',
        message: response.data.message || 'Error generating diagram'
      });
    }

    // Return the mermaid code from the backend
    return res.status(200).json({
      success: true,
      mermaid_code: response.data.mermaid_code || response.data,
      message: response.data.message || 'Diagram generated successfully'
    });
  } catch (error) {
    console.error('Error generating diagram:', error.message);
    if (error.response) {
      console.error('Backend error response:', error.response.data);
    }
    
    // Handle different types of errors
    if (error.response) {
      // The backend returned an error response
      return res.status(error.response.status || 500).json({ 
        success: false,
        error: 'backend_error',
        message: error.response.data?.message || error.response.data?.detail || 'Backend error' 
      });
    } else if (error.request) {
      // The request was made but no response was received
      return res.status(503).json({ 
        success: false,
        error: 'service_unavailable', 
        message: 'Could not connect to diagram generation service. Please make sure the backend is running.' 
      });
    } else {
      // Something happened in setting up the request
      return res.status(500).json({ 
        success: false,
        error: 'internal_error',
        message: `Internal server error: ${error.message}` 
      });
    }
  }
} 