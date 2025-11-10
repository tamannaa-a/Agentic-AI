import React, { useState } from "react"
import UploadCard from "./UploadCard"
import SummaryPanel from "./SummaryPanel"
import AnalyticsTab from "./AnalyticsTab"
import FlowGraph from "./FlowGraph"

export default function NeonTabs({ result, setResult }){
  const [tab, setTab] = useState("claim")

  return (
    <div className="space-y-6">
      <div className="flex gap-3">
        <button onClick={()=>setTab("claim")} className={`px-4 py-2 rounded-xl ${tab==="claim" ? "tab-active bg-[#07182b]" : "bg-transparent"} text-sm`}>Claim Summary</button>
        <button onClick={()=>setTab("analytics")} className={`px-4 py-2 rounded-xl ${tab==="analytics" ? "tab-active bg-[#07182b]" : "bg-transparent"} text-sm`}>Fraud Analytics</button>
        <button onClick={()=>setTab("flow")} className={`px-4 py-2 rounded-xl ${tab==="flow" ? "tab-active bg-[#07182b]" : "bg-transparent"} text-sm`}>Processing Flow</button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2">
          {tab === "claim" && <UploadCard onResult={setResult} />}
          {tab === "analytics" && <AnalyticsTab data={result} />}
          {tab === "flow" && <FlowGraph graph={result?.graph} />}
        </div>

        <aside className="space-y-6">
          <div className="card p-4">
            <h4 className="text-sm text-slate-300">Quick Actions</h4>
            <div className="mt-3 space-y-2">
              <button className="btn-neon w-full">Export Report (PDF)</button>
              <button className="btn-neon w-full">Mark for Review</button>
            </div>
          </div>

          <div className="card p-4">
            <h4 className="text-sm text-slate-300">Last Result</h4>
            {result ? (
              <div className="mt-2">
                <div className="small">Claim</div>
                <div className="text-sm font-semibold">{result.extracted?.claim_id || '—'}</div>
                <div className="small mt-2">Fraud Score</div>
                <div className="text-lg font-bold">{((result.fraud?.score||0)*100).toFixed(1)}%</div>
              </div>
            ) : <div className="small mt-2">No analysis yet</div>}
          </div>
        </aside>
      </div>

      {tab === "claim" && result && <SummaryPanel data={result} />}
    </div>
  )
}
