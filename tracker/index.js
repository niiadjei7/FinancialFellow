// index.js
const express = require('express');
const axios = require('axios');
const { ChartJSNodeCanvas } = require('chartjs-node-canvas');

const app = express();
const port = 3000;

const canvasRenderService = new ChartJSNodeCanvas({ width: 800, height: 400 });

app.get('/', async (req, res) => {
  try {
    const response = await axios.get('http://localhost:8000/api/budget_data/');
    const budgetData = response.data;

    const chartConfiguration = {
      type: 'bar',
      data: {
        labels: budgetData.labels,
        datasets: [{
          label: 'Budget Amounts',
          data: budgetData.amounts,
          backgroundColor: 'blue',
        }],
      },
      options: {
        scales: {
          x: {
            ticks: {
              color: 'white', // X-axis label color
            },
          },
          y: {
            ticks: {
              color: 'white', // Y-axis label color
            },
          },
        },
      },
    };

    const image = await canvasRenderService.renderToBuffer(chartConfiguration);
    res.writeHead(200, { 'Content-Type': 'image/png' });
    res.end(image, 'binary');
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
