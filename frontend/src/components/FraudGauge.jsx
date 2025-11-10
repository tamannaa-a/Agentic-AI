import React from "react"
import { RadialBarChart, RadialBar, ResponsiveContainer } from "recharts"

export default function FraudGauge({ score = 0 }) {
  const riskLevel = score > 0.75 ? "High" : score > 0.4 ? "Medium" : "Low"
  const color = riskLevel === "High" ? "#ef4444" : riskLevel === "Medium" ? "#f59e0b" : "#10b981"
  const data = [{ name: "Risk", uv: Math.round(score * 100), fill: color }]

  return (
    <div className="mt-6 text-center">
      <h3 className="text-lg font-semibold text-gray-700 mb-2">Fraud Risk Assessment</h3>
      <div className="flex justify-center items-center">
        <ResponsiveContainer width={250} height={180}>
          <RadialBarChart cx="50%" cy="50%" innerRadius="60%" outerRadius="100%" barSize={16} data={data}>
            <RadialBar background dataKey="uv" cornerRadius={50} />
          </RadialBarChart>
        </ResponsiveContainer>
      </div>
      <p className="text-gray-700 font-medium">Risk Level: <span style={{ color }}>{riskLevel}</span></p>
      <p className="text-sm text-gray-500">Score: {(score * 100).toFixed(1)}%</p>
    </div>
  )
}
