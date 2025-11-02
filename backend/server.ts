import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import ocrRoutes from './routes/ocr.js';
import serverRoutes from './routes/servers.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors({
  origin: process.env.CORS_ORIGIN || '*',
  credentials: true
}));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Routes
app.use('/api/ocr', ocrRoutes);
app.use('/api', serverRoutes);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'OCR Backend' });
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`?? OCR Backend server running on http://0.0.0.0:${PORT}`);
  console.log(`?? GCP Credentials: ${process.env.GOOGLE_APPLICATION_CREDENTIALS || 'Using default'}`);
});

export default app;
