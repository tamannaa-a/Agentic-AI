import React, {useState} from "react";
import axios from "axios";
import "./index.css";

function App(){
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";

  const handleUpload = async (e) => {
    setFile(e.target.files[0]);
  }

  const handleClassify = async () => {
    if(!file) return alert("Upload a PDF first");
    const form = new FormData();
    form.append("file", file);

    try{
      setLoading(true);
      const resp = await axios.post(`${apiUrl}/classify`, form, {
        headers: {"Content-Type": "multipart/form-data"}
      });
      setResult(resp.data);
    } catch(err){
      console.error(err);
      alert(err?.response?.data?.detail || "Classification failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
      <div className="bg-white shadow rounded p-6 w-full max-w-3xl">
        <h1 className="text-2xl font-bold mb-4">Agentic AI — Document Classifier</h1>
        <input type="file" accept="application/pdf" onChange={handleUpload} />
        <div className="mt-4">
          <button onClick={handleClassify} disabled={loading || !file}
            className="bg-blue-600 text-white px-4 py-2 rounded">
            {loading ? "Analyzing..." : "Classify Document"}
          </button>
        </div>

        {result && (
          <div className="mt-6">
            <h2 className="text-lg font-semibold">Result</h2>
            <p><b>Type:</b> {result.label}</p>
            <p><b>Confidence:</b> {result.confidence.toFixed(3)}</p>
            <h3 className="mt-2 font-semibold">Fields</h3>
            <pre className="bg-gray-100 p-3 rounded">{JSON.stringify(result.fields, null, 2)}</pre>
            <details className="mt-2">
              <summary>Text Preview</summary>
              <pre className="bg-gray-100 p-3 rounded max-h-60 overflow-auto">{result.text_preview}</pre>
            </details>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
