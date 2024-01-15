function initChart(chartData) {
  const width = 800;
  const height = 800;

  const svg = d3.select('#pie-chart')
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${width / 2},${height / 2})`);

  const pie = d3.pie();
  const arc = d3.arc().innerRadius(0).outerRadius(Math.min(width, height) / 2);

  const color = d3.scaleOrdinal(d3.schemeCategory10);

  const pieData = pie(chartData.data);

  // Append paths for the pie chart segments
  svg.selectAll('path')
      .data(pieData)
      .enter()
      .append('path')
      .attr('d', arc)
      .attr('fill', (d, i) => color(i))
      .attr('stroke', 'white')
      .style('stroke-width', '2px');

  // Append text labels for each segment
  svg.selectAll('text')
      .data(pieData)
      .enter()
      .append('text')
      .text((d, i) => `${chartData.labels[i]}: ${Math.round((d.data / d3.sum(chartData.data)) * 100)}%`) // Include label and percentage
      .attr('transform', d => `translate(${arc.centroid(d)})`) // Position at the centroid
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em') // Offset for better positioning
      .style('font-size', '20px')
      .style('fill', 'white'); // Adjust styling as needed
}