import React from "react"
import FraudGauge from "./FraudGauge"

export default function SummaryPanel({ data }) {
  const { extracted, validation, fraud, explanation } = data

  return (
    <div className="panel space-y-4">
      <h2 className="text-xl font-semibold text-gray-800">Claim Analysis Summary</h2>
      <div className="grid md:grid-cols-2 gap-6">
        <div>
          <h3 className="font-medium text-gray-700 mb-1">Extracted Entities</h3>
          <pre className="json-box">{JSON.stringify(extracted, null, 2)}</pre>
        </div>
        <div>
          <h3 className="font-medium text-gray-700 mb-1">Policy Validation</h3>
          <pre className="json-box">{JSON.stringify(validation, null, 2)}</pre>
        </div>
      </div>
      <FraudGauge score={fraud.score} />
      <div>
        <h3 className="font-medium text-gray-700 mb-1">System Explanation</h3>
        <pre className="bg-blue-50 border border-blue-200 text-gray-800 text-sm p-4 rounded-lg overflow-auto">
          {explanation.explanation}
        </pre>
      </div>
    </div>
  )
}
