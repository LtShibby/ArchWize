import { useState, useEffect, useRef } from "react";
import axios from "axios";
import Head from 'next/head';
import mermaid from "mermaid";

export default function Home() {
    const [input, setInput] = useState("");
    const [diagram, setDiagram] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");
    const diagramRef = useRef(null);

    useEffect(() => {
        // Initialize mermaid
        mermaid.initialize({
            startOnLoad: true,
            theme: 'default',
            securityLevel: 'loose',
        });
    }, []);

    useEffect(() => {
        if (diagram) {
            try {
                // Clear previous diagram
                if (diagramRef.current) {
                    diagramRef.current.innerHTML = diagram;
                }
                // Parse diagram
                mermaid.contentLoaded();
            } catch (err) {
                console.error("Failed to render diagram:", err);
                setError("Failed to render diagram. Please check the syntax.");
            }
        }
    }, [diagram]);

    const generateDiagram = async () => {
        if (!input.trim()) {
            setError("Please enter a description for your diagram");
            return;
        }

        setIsLoading(true);
        setError("");
        
        try {
            const response = await axios.post("/api/generate", { prompt: input });
            setDiagram(response.data.mermaid_code);
        } catch (err) {
            console.error("Error generating diagram:", err);
            setError(err.response?.data?.detail || "Failed to generate diagram");
        } finally {
            setIsLoading(false);
        }
    };
    
    return (
        <div className="container">
            <Head>
                <title>ArchWize - AI-Powered Diagram Generator</title>
                <meta name="description" content="Generate architecture diagrams with AI" />
                <link rel="icon" href="/favicon.ico" />
            </Head>

            <main className="main">
                <h1 className="title">
                    <span className="highlight">Arch</span>Wize
                </h1>
                <p className="description">
                    AI-Powered Diagram & Architecture Flowchart Generator
                </p>

                <div className="input-section">
                    <textarea 
                        className="prompt-input"
                        placeholder="Describe the diagram you want to create... (e.g., 'Create a flowchart for user registration process')"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        rows={5}
                    />
                    <button 
                        className="generate-btn"
                        onClick={generateDiagram}
                        disabled={isLoading}
                    >
                        {isLoading ? 'Generating...' : 'Generate Diagram'}
                    </button>
                </div>

                {error && <div className="error">{error}</div>}

                <div className="diagram-section">
                    {diagram && (
                        <>
                            <h2>Your Diagram</h2>
                            <div ref={diagramRef} className="mermaid">
                                {diagram}
                            </div>
                        </>
                    )}
                </div>
            </main>

            <footer className="footer">
                <p>Powered by ArchWize &copy; {new Date().getFullYear()}</p>
            </footer>

            <style jsx>{`
                .container {
                    min-height: 100vh;
                    padding: 0 0.5rem;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    background-color: #f5f5f5;
                }
                .main {
                    padding: 5rem 0;
                    flex: 1;
                    display: flex;
                    flex-direction: column;
                    justify-content: flex-start;
                    align-items: center;
                    max-width: 1000px;
                    width: 100%;
                }
                .title {
                    margin: 0;
                    line-height: 1.15;
                    font-size: 4rem;
                    text-align: center;
                }
                .highlight {
                    color: #0070f3;
                }
                .description {
                    text-align: center;
                    line-height: 1.5;
                    font-size: 1.5rem;
                    margin: 1rem 0 2rem;
                }
                .input-section {
                    width: 100%;
                    margin-bottom: 2rem;
                }
                .prompt-input {
                    width: 100%;
                    padding: 1rem;
                    font-size: 1rem;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    margin-bottom: 1rem;
                    resize: vertical;
                }
                .generate-btn {
                    padding: 0.75rem 1.5rem;
                    background-color: #0070f3;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 1rem;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }
                .generate-btn:hover {
                    background-color: #0051a3;
                }
                .generate-btn:disabled {
                    background-color: #ccc;
                    cursor: not-allowed;
                }
                .diagram-section {
                    width: 100%;
                    margin-top: 2rem;
                    padding: 1rem;
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }
                .error {
                    color: #e74c3c;
                    margin: 1rem 0;
                    padding: 0.75rem;
                    background-color: #ffeaea;
                    border-radius: 5px;
                    width: 100%;
                }
                .footer {
                    width: 100%;
                    height: 100px;
                    border-top: 1px solid #eaeaea;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
            `}</style>
        </div>
    );
} 