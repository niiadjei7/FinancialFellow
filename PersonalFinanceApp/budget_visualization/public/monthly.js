function initChart(labels, data) {
    monthlyData = {
        'labels': labels,
        'data' :  data
    }
    const margin = { top: 30, right: 30, bottom: 30, left: 60 };
    const width = 800 - margin.left - margin.right;
    const height = 800 - margin.top - margin.bottom;

    const svg = d3.select('#line-chart')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    const parseTime = d3.timeParse('%Y-%m');
    const formatDate = d3.timeFormat('%b %Y');

    const x = d3.scaleTime()
        .domain(d3.extent(labels, d => parseTime(d)))
        .range([0, width]);

    const y = d3.scaleLinear()
        .domain([0, 200])
        .range([height, 0]);

    console.log(x.domain())
    console.log(y.domain())

    const line = d3.line()
        .x(d => x(parseTime(d.month_year)))
        .y(d => y(d.total));

    console.log(line.x())
    console.log(line.y())

    svg.append('path')
        .datum(monthlyData)
        .attr('fill', 'none')
        .attr('stroke', 'steelblue')
        .attr('stroke-width', 5)
        .attr('d', line);

    // Add x-axis
    svg.append('g')
        .attr('transform', 'translate(0,' + height + ')')
        .call(d3.axisBottom(x).ticks(d3.timeMonth.every(1)).tickFormat(formatDate));

    // Add y-axis
    svg.append('g')
        .call(d3.axisLeft(y));

    // Add labels
    svg.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('y', 0 - margin.left)
        .attr('x', 0 - (height / 2))
        .attr('dy', '1em')
        .style('text-anchor', 'middle')
        .text('Total Expenses');

    svg.append('text')
        .attr('transform', 'translate(' + (width / 2) + ' ,' + (height + margin.top) + ')')
        .style('text-anchor', 'middle')
        .text('Date');
}