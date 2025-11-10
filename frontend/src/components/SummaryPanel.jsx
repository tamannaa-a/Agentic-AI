import React from "react"
import FraudGaugeEcharts from "./FraudGaugeEcharts"

export default function SummaryPanel({ data }){
  const { extracted, validation, fraud, explanation } = data || {}
  return (
    <div className="card p-6 mt-6">
      <h3 className="text-xl font-semibold mb-3">Claim Analysis Summary</h3>
      <div className="grid md:grid-cols-3 gap-6">
        <div className="md:col-span-2">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <h4 className="small">Extracted Entities</h4>
              <div className="json-box mt-2">{JSON.stringify(extracted,null,2)}</div>
            </div>
            <div>
              <h4 className="small">Policy Validation</h4>
              <div className="json-box mt-2">{JSON.stringify(validation,null,2)}</div>
            </div>
          </div>

          <div className="mt-4">
            <h4 className="small">System Explanation</h4>
            <div className="bg-black/20 p-3 rounded mt-2">{explanation?.explanation}</div>
          </div>
        </div>

        <div>
          <FraudGaugeEcharts score={fraud?.score || 0} />
        </div>
      </div>
    </div>
  )
}
