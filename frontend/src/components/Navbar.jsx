import React from "react"
import { Brain } from "lucide-react"

export default function Navbar(){
  return (
    <header className="py-4">
      <div className="max-w-7xl mx-auto flex items-center gap-4 px-4">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg" style={{background: 'radial-gradient(circle at 10% 20%, rgba(0,229,255,0.12), rgba(196,0,255,0.06))'}}>
            <Brain className="text-[#00e5ff]" size={28} />
          </div>
          <div>
            <div className="text-2xl font-bold logo-mark">Claims Intelligence Dashboard</div>
            <div className="text-sm small">Dark neon demo • Offline</div>
          </div>
        </div>
        <div className="ml-auto flex items-center gap-3">
          <div className="text-sm kv">Status: <span className="text-green-400 ml-2">Running</span></div>
        </div>
      </div>
    </header>
  )
}
