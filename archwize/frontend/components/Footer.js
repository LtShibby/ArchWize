import React from 'react';

export const Footer = () => {
  return (
    <footer className="footer-container">
      <div className="footer-content">
        <p className="footer-copyright">
          © {new Date().getFullYear()}{" "}
          <a 
            href="https://wozwize.com" 
            target="_blank" 
            rel="noopener noreferrer"
            className="footer-brand-link"
          >
            WozWize
          </a>. All Rights Reserved.
        </p>
        
        <div className="footer-links footer-space-y">
          <a 
            href="https://wozwize.com/privacy-policy" 
            target="_blank"
            rel="noopener noreferrer"
            className="footer-link"
          >
            Privacy Policy
          </a>
          <a 
            href="https://wozwize.com/terms-of-service"
            target="_blank"
            rel="noopener noreferrer" 
            className="footer-link"
          >
            Terms of Service
          </a>
          <a 
            href="https://wozwize.com/about"
            target="_blank"
            rel="noopener noreferrer"
            className="footer-link"
          >
            About Us
          </a>
        </div>
      </div>
    </footer>
  );
}; 