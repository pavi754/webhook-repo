const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(bodyParser.json());

// Serve static files like ui.html
app.use('/', express.static(path.join(__dirname)));

let events = [];

app.post('/webhook', (req, res) => {
  const eventType = req.headers['x-github-event'];
  const payload = req.body;

  if (eventType === 'push') {
    const time = payload.head_commit.timestamp;
    const message = payload.head_commit.message;
    const pusher = payload.pusher.name;
    const repo = payload.repository.full_name;

    // Avoid duplicates based on timestamp
    const exists = events.find(e => e.timestamp === time);
    if (!exists) {
      events.push({ time, message, pusher, repo });
      console.log(`📦 New Push: [${repo}] by ${pusher} - "${message}" at ${time}`);
    }
  }

  res.sendStatus(200);
});

// API to get stored events
app.get('/events', (req, res) => {
  res.json(events);
});

app.listen(PORT, () => {
  console.log(`🚀 Webhook server running at http://localhost:${PORT}`);
});
