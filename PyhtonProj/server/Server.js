// server.js - Basic Express server
const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const port = 3000;

// Serve static files from 'public' directory
app.use(express.static('public'));

// API endpoint to get all data
app.get('/api/data', (req, res) => {
  try {
    // Read the JSON data file
    const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'data', 'azure_data.json'), 'utf8'));
    res.json(data);
  } catch (error) {
    console.error('Error reading data:', error);
    res.status(500).json({ error: 'Failed to load data' });
  }
});

// API endpoint to get activity data
app.get('/api/activities', (req, res) => {
  try {
    // Read the CSV file and convert to JSON
    const csv = fs.readFileSync(path.join(__dirname, 'data', 'azure_activities.csv'), 'utf8');
    
    // Very basic CSV to JSON conversion (in a real app, use a proper CSV parser)
    const lines = csv.split('\n');
    const headers = lines[0].split(',');
    
    const data = lines.slice(1).map(line => {
      const values = line.split(',');
      return headers.reduce((obj, header, index) => {
        obj[header] = values[index];
        return obj;
      }, {});
    });
    
    res.json(data);
  } catch (error) {
    console.error('Error reading activities:', error);
    res.status(500).json({ error: 'Failed to load activity data' });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
