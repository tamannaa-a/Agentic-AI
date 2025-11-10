import React, { useState } from 'react'

export default function UploadForm({ onResult }) {
  const [text, setText] = useState('')
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)

  const submit = async (e) => {
    e.preventDefault()
    setLoading(true)
    const form = new FormData()
    if (file) form.append('file', file)
    form.append('text', text)

    try {
      const res = await fetch('http://127.0.0.1:8000/analyze', {
        method: 'POST',
        body: form
      })
      const data = await res.json()
      onResult(data)
    } catch (err) {
      console.error(err)
      alert('Error connecting to backend')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={submit} className="upload-form">
      <label>Paste claim text (or upload a PDF):</label>
      <textarea value={text} onChange={(e) => setText(e.target.value)} placeholder="Claim text..." />
      <input type="file" accept=".pdf,.txt" onChange={(e) => setFile(e.target.files[0])} />
      <button type="submit" disabled={loading}>{loading ? 'Analyzing...' : 'Analyze Claim'}</button>
    </form>
  )
}
