import '../styles/globals.css';
import Head from 'next/head';

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta name="description" content="ArchWize - AI-Powered Diagram & Architecture Flowchart Generator" />
        <meta name="keywords" content="diagram, architecture, flowchart, AI, mermaid, visualization" />
        <title>ArchWize</title>
      </Head>
      <Component {...pageProps} />
    </>
  );
}

export default MyApp; 