import React from "react"
import ReactECharts from "echarts-for-react"

export default function FraudGaugeEcharts({ score = 0 }){
  const pct = Math.round(score * 100)
  const level = score > 0.75 ? 'High' : score > 0.4 ? 'Medium' : 'Low'
  const color = score > 0.75 ? '#ff4d4f' : score > 0.4 ? '#f59e0b' : '#10b981'

  const option = {
    backgroundColor: 'transparent',
    series: [
      {
        type: 'gauge',
        startAngle: 180,
        endAngle: 0,
        min: 0,
        max: 100,
        progress: { show: true, width: 18, itemStyle: { color } },
        axisLine: { lineStyle: { width: 18, color: [[1, '#073044']] } },
        pointer: { show: false },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { show: false },
        detail: {
          valueAnimation: true,
          formatter: ['{value}%','{level|'+level+'}'].join('\n'),
          rich: {
            level: { color, fontSize: 12, padding: [6,0,0,0] }
          },
          color: '#e6eef8',
          fontSize: 16
        },
        data: [{ value: pct }]
      }
    ]
  }

  return (
    <div className="p-4 card text-center">
      <h4 className="small">Fraud Risk</h4>
      <div style={{height:200}}>
        <ReactECharts option={option} style={{height:'100%'}} />
      </div>
      <div className="mt-2 small">Score: <span className="font-semibold">{pct}%</span></div>
    </div>
  )
}
