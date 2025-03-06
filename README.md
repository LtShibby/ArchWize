# ArchWize - AI-Powered Diagram & Architecture Flowchart SaaS

ArchWize is a SaaS application that uses AI to generate diagrams and architecture flowcharts from text descriptions. It leverages the free Hugging Face Inference API with Mistral-7B model to convert natural language into Mermaid.js syntax for rendering beautiful diagrams.

## Features

- 🧠 AI-powered diagram generation from text descriptions
- 📊 Support for multiple diagram types (flowcharts, sequence diagrams, class diagrams, etc.)
- 🎨 Clean, modern UI for a great user experience
- 📱 Responsive design that works on desktop and mobile
- 🔄 Real-time diagram rendering with Mermaid.js
- 💰 **Completely free** - Uses Hugging Face's free tier API

## Tech Stack

- **Frontend**: Next.js, React, Mermaid.js
- **Backend**: FastAPI (Python)
- **AI**: Hugging Face Inference API with Mistral-7B model
- **Deployment**: Vercel (or your preferred hosting)

## Project Structure

```
archwize/
│── backend/          # FastAPI backend
│   ├── main.py       # FastAPI app
│   ├── config.py     # Environment variables
│   ├── services.py   # AI processing logic
│   ├── models.py     # Data models
│   ├── requirements.txt  # Python dependencies
│── frontend/         # Next.js frontend
│   ├── pages/
│   │   ├── index.js  # Homepage
│   │   ├── _app.js   # Next.js app setup
│   │   ├── api/
│   │       ├── generate.js  # API route
│   ├── styles/
│   │   ├── globals.css  # Global styles
│── .env             # Environment variables
│── README.md        # Project documentation
```

## Getting Started

### Prerequisites

- Node.js (v14+)
- Python (v3.8+)
- No API keys required! This project uses Hugging Face's free tier

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/archwize.git
cd archwize
```

2. **Set up the backend**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Set up the frontend**

```bash
cd ../frontend
npm install
```

4. **Configure environment variables**

Create a `.env` file in the root directory with the following:

```
# No API keys required for basic functionality!
DEBUG=true
PORT=8000
HOST=0.0.0.0
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
BACKEND_URL=http://localhost:8000
```

### Running the Application

1. **Start the backend**

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload
```

2. **Start the frontend**

```bash
cd frontend
npm run dev
```

3. **Access the application**

Open your browser and navigate to `http://localhost:3000`

## Deployment

### Backend (FastAPI)

Deploy the FastAPI backend to Vercel serverless functions:

```bash
cd backend
vercel deploy
```

### Frontend (Next.js)

Deploy the Next.js frontend to Vercel:

```bash
cd frontend
vercel deploy
```

## Future Enhancements

- User authentication
- Saved diagrams
- Premium features with Stripe integration
- More diagram types and customization options
- Optional integration with paid AI services for higher quality diagrams

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Hugging Face](https://huggingface.co/) for the free Inference API
- [Mistral AI](https://mistral.ai/) for the open-source Mistral-7B model
- [Mermaid.js](https://mermaid-js.github.io/mermaid/) for diagram rendering
- [FastAPI](https://fastapi.tiangolo.com/) and [Next.js](https://nextjs.org/) for the awesome frameworks