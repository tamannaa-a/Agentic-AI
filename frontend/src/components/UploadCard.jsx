import React, { useState } from "react"
import { UploadCloud, Loader2 } from "lucide-react"

export default function UploadCard({ onResult }) {
  const [text, setText] = useState("")
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    const form = new FormData()
    if (file) form.append("file", file)
    form.append("text", text)
    try {
      const res = await fetch("http://127.0.0.1:8000/claims/analyze", {
        method: "POST",
        body: form,
      })
      const data = await res.json()
      onResult(data)
    } catch (err) {
      alert("Backend not reachable")
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="panel">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex items-center gap-3">
          <UploadCloud className="text-blue-600" />
          <h2 className="text-lg font-semibold text-gray-800">Upload / Paste Claim</h2>
        </div>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste claim text..."
          className="w-full rounded-lg border-gray-300 focus:ring-blue-500 focus:border-blue-500 p-3"
          rows={5}
        />
        <input type="file" accept=".pdf,.txt" onChange={(e) => setFile(e.target.files[0])} />
        <div className="flex gap-3">
          <button type="submit" disabled={loading} className="flex items-center gap-2">
            {loading && <Loader2 className="animate-spin" size={16} />}
            {loading ? "Analyzing..." : "Analyze Claim"}
          </button>
        </div>
      </form>
    </div>
  )
}
