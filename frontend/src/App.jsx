import React, { useState } from "react"
import Navbar from "./components/Navbar"
import UploadCard from "./components/UploadCard"
import SummaryPanel from "./components/SummaryPanel"
import FlowGraph from "./components/FlowGraph"

export default function App() {
  const [result, setResult] = useState(null)

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-6xl mx-auto px-6 py-10 space-y-8">
        <UploadCard onResult={setResult} />
        {result && (
          <>
            <SummaryPanel data={result} />
            <FlowGraph graph={result.graph} />
          </>
        )}
      </div>
    </div>
  )
}
