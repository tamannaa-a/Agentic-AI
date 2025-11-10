import React, { useEffect, useRef } from 'react'
import * as d3 from 'd3'

export default function DecisionGraph({ graph }) {
  const ref = useRef()

  useEffect(() => {
    if (!graph) return
    const width = 800
    const height = 400
    const svg = d3.select(ref.current)
    svg.selectAll('*').remove()

    const nodes = graph.nodes.map(n => ({ id: n.id, label: n.label, meta: n.meta }))
    const links = graph.edges.map(e => ({ source: e.from, target: e.to }))

    const sim = d3.forceSimulation(nodes)
      .force('charge', d3.forceManyBody().strength(-400))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('link', d3.forceLink(links).id(d => d.id).distance(120))

    const link = svg.append('g')
      .attr('stroke', '#999')
      .selectAll('line')
      .data(links)
      .enter().append('line')
      .attr('stroke-width', 2)

    const node = svg.append('g')
      .selectAll('g')
      .data(nodes)
      .enter().append('g')
      .call(d3.drag()
        .on('start', (event, d) => {
          if (!event.active) sim.alphaTarget(0.3).restart()
          d.fx = d.x
          d.fy = d.y
        })
        .on('drag', (event, d) => {
          d.fx = event.x
          d.fy = event.y
        })
        .on('end', (event, d) => {
          if (!event.active) sim.alphaTarget(0)
          d.fx = null
          d.fy = null
        })
      )

    node.append('circle')
      .attr('r', 28)
      .attr('fill', '#ffffff')
      .attr('stroke', '#333')
      .attr('stroke-width', 2)

    node.append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', 5)
      .text(d => d.label)

    node.append('title').text(d => JSON.stringify(d.meta, null, 2))

    sim.on('tick', () => {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y)

      node.attr('transform', d => `translate(${d.x},${d.y})`)
    })

    return () => sim.stop()
  }, [graph])

  return <svg ref={ref} width={800} height={400} />
}
