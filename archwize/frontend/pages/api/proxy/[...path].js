import { createProxyMiddleware } from 'http-proxy-middleware';

// This proxy middleware forwards API requests to our Python backend
export default function handler(req, res) {
  const target = process.env.BACKEND_URL || 'http://localhost:8000';
  const path = req.url.replace('/api/proxy', '');
  
  // Forward the request
  fetch(`${target}${path}`, {
    method: req.method,
    headers: {
      'Content-Type': 'application/json',
      ...req.headers,
    },
    body: req.method !== 'GET' && req.method !== 'HEAD' ? JSON.stringify(req.body) : undefined,
  })
    .then(async (response) => {
      // Copy status and headers
      res.statusCode = response.status;
      for (const [key, value] of response.headers.entries()) {
        res.setHeader(key, value);
      }
      
      // Parse and send the response body
      const data = await response.json();
      res.json(data);
    })
    .catch((error) => {
      console.error('API proxy error:', error);
      res.status(500).json({ error: 'Failed to fetch from API backend' });
    });
} 