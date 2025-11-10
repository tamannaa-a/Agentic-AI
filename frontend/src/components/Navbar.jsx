import React from "react"
import { Brain } from "lucide-react"

export default function Navbar() {
  return (
    <nav className="bg-white shadow-sm sticky top-0 z-50">
      <div className="max-w-6xl mx-auto flex items-center gap-3 px-6 py-3">
        <Brain className="text-blue-600" size={28} />
        <h1 className="text-xl font-bold text-gray-800">Claims Intelligence Dashboard</h1>
        <div className="ml-auto flex items-center gap-4 text-sm text-gray-500">
          Demo • Offline
        </div>
      </div>
    </nav>
  )
}
