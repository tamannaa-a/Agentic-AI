import React, { useState } from "react"
import Navbar from "./components/Navbar"
import NeonTabs from "./components/NeonTabs"
import './styles.css'

export default function App(){
  const [result, setResult] = useState(null)

  return (
    <div className="min-h-screen bg-[#071025] font-sans">
      <Navbar />
      <main className="max-w-7xl mx-auto px-6 py-8">
        <NeonTabs result={result} setResult={setResult} />
      </main>
      <footer className="text-center text-xs text-slate-400 pb-6">Intelligent Claims Orchestrator — Demo (Offline)</footer>
    </div>
  )
}
