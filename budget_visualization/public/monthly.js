function initChart(labels, data) {


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

    // Insert the initial point (0, 0) to connect the line to the starting point
    const initialData = [{ month_year: labels[0], total: 0 }];
    const combinedData = initialData.concat(
        labels.map((label, index) => ({
            month_year: label,
            total: data[index],
        }))
    );

    const x = d3.scaleTime()
        .domain(d3.extent(combinedData, d => parseTime(d.month_year)))
        .range([0, width]);

    const y = d3.scaleLinear()
        .domain([0, d3.max(data) + 50])
        .range([height, 0]);

    const line = d3.line()
        .x(d => x(parseTime(d.month_year)))
        .y(d => y(d.total));

    svg.append('path')
        .datum(combinedData)
        .attr('fill', 'none')
        .attr('stroke', 'steelblue')
        .attr('stroke-width', 2)
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

    svg.selectAll('dot')
        .data(combinedData)
        .enter().append('circle')
        .attr('r', 6)  // Adjust the radius for bigger dots
        .attr('cx', d => x(parseTime(d.month_year)))
        .attr('cy', d => y(d.total))
        .style('fill', 'steelblue');

    svg.selectAll('dot-label')
        .data(combinedData)
        .enter().append('text')
        .attr('x', d => x(parseTime(d.month_year)))
        .attr('y', d => y(d.total))
        .attr('dy', -10)  // Adjust the vertical position of the label
        .attr('text-anchor', 'middle')
        .text(d => '$'+d.total.toFixed(2));
}