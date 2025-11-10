import React, { useState } from "react"
import { Loader2, UploadCloud } from "lucide-react"

export default function UploadCard({ onResult }){
  const [text, setText] = useState("")
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState(null)

  const submit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage(null)
    const form = new FormData()
    if (file) form.append('file', file)
    form.append('text', text)
    try {
      const res = await fetch('http://127.0.0.1:8000/claims/analyze', { method: 'POST', body: form })
      if(!res.ok) throw new Error('Backend error')
      const data = await res.json()
      onResult(data)
      setMessage({type:'success', text:'Analysis complete'})
    } catch(err){
      setMessage({type:'error', text: err.message || 'Connection error'})
    } finally { setLoading(false) }
  }

  return (
    <div className="card p-6">
      <div className="flex items-center gap-3">
        <div className="p-3 rounded-lg" style={{background: 'linear-gradient(90deg,#002b3a,#2b003a)'}}>
          <UploadCloud className="text-[#00e5ff]" />
        </div>
        <h3 className="text-lg font-semibold">Upload / Paste Claim</h3>
      </div>

      <form onSubmit={submit} className="mt-4 space-y-4">
        <textarea value={text} onChange={(e)=>setText(e.target.value)} placeholder="Paste claim text..." className="w-full rounded-md p-3 bg-transparent border border-transparent focus:border-[#00495a] resize-none" rows={6} />
        <input type="file" accept=".pdf,.txt" onChange={(e)=>setFile(e.target.files[0])} />
        <div className="flex items-center gap-3">
          <button type="submit" disabled={loading} className="btn-neon inline-flex items-center gap-2">
            {loading ? <Loader2 className="animate-spin" /> : null}
            Analyze Claim
          </button>
          {message && (
            <div className={`text-sm ${message.type==='success' ? 'text-green-300' : 'text-rose-400'}`}>{message.text}</div>
          )}
        </div>
      </form>
    </div>
  )
}
