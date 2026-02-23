const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;
const CONTENT_FILE = path.join(__dirname, 'content.txt');

app.use(express.static(path.join(__dirname, 'public')));

app.get('/api/summary', (req, res) => {
  fs.readFile(CONTENT_FILE, 'utf8', (err, data) => {
    if (err) {
      return res.status(500).json({ error: 'Could not read content.txt' });
    }
    res.json({ summary: data.trim() });
  });
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
