import React, { useState } from 'react'
import UploadForm from './components/UploadForm'
import DecisionGraph from './components/DecisionGraph'

export default function App() {
  const [result, setResult] = useState(null)

  return (
    <div className="container">
      <h1>Intelligent Claims Orchestrator</h1>
      <div className="panel">
        <UploadForm onResult={setResult} />
      </div>
      {result && (
        <div className="panel">
          <h2>Result Summary</h2>
          <pre className="json-box">{JSON.stringify(result.explanation, null, 2)}</pre>
          <h3>Extracted Fields</h3>
          <pre className="json-box">{JSON.stringify(result.extracted, null, 2)}</pre>
          <h3>Decision Graph</h3>
          <DecisionGraph graph={result.graph} />
        </div>
      )}
    </div>
  )
}
