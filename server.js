const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

app.disable('x-powered-by');

app.use((_, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader('Permissions-Policy', 'camera=(self), microphone=(self), geolocation=()');
  next();
});

app.get('/', (_, res) => {
  res.sendFile(path.join(__dirname, 'solivana-branded.html'));
});

app.get('/healthz', (_, res) => res.json({ ok: true }));

app.use(express.static(__dirname, {
  index: false,
  maxAge: '1h',
  setHeaders: (res, filePath) => {
    if (filePath.endsWith('.html')) res.setHeader('Cache-Control', 'no-cache');
  }
}));

app.use((_, res) => {
  res.status(404).sendFile(path.join(__dirname, 'solivana-branded.html'));
});

app.listen(PORT, () => {
  console.log(`SoliVana ZYTO listening on :${PORT}`);
});
