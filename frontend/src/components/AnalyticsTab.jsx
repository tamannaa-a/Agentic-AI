import React from "react"
import ReactECharts from "echarts-for-react"

/* Small demo analytics: claim counts / fraud trend */
export default function AnalyticsTab({ data }){
  // demo synthetic series (replace with real)
  const days = Array.from({length:12}, (_,i)=>`D-${11-i}`)
  const claims = [12,9,15,11,14,13,10,18,16,11,9,7]
  const fraudRate = [0.12,0.09,0.16,0.14,0.11,0.09,0.08,0.2,0.17,0.12,0.09,0.05].map(v=>v*100)

  const option = {
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis' },
    legend: { textStyle: { color: '#cfefff' } },
    xAxis: { type: 'category', data: days, axisLine: { lineStyle: { color: '#2f4f5f' } } },
    yAxis: [{ type: 'value', name: 'Claims', position: 'left' },
            { type: 'value', name: 'Fraud %', position: 'right' }],
    series: [
      { name: 'Claims', type: 'bar', data: claims, itemStyle: { color: '#00e5ff' }, barGap: 0 },
      { name: 'Fraud %', type: 'line', data: fraudRate, yAxisIndex:1, itemStyle: { color: '#c400ff' }, smooth: true }
    ]
  }

  return (
    <div className="card p-4">
      <h3 className="text-lg font-semibold mb-3">Fraud Analytics</h3>
      <ReactECharts option={option} style={{height:360}} />
    </div>
  )
}
