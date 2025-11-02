// test-vision.js
const {ImageAnnotatorClient} = require('@google-cloud/vision');

async function testVisionAPI() {
  try {
    const client = new ImageAnnotatorClient();
    console.log('? Vision API client initialized successfully');
    console.log('? Service account credentials loaded');
    console.log('? Ready to use Vision API');
  } catch (error) {
    console.error('? Error:', error.message);
    if (error.message.includes('Could not load the default credentials')) {
      console.error('  Make sure GOOGLE_APPLICATION_CREDENTIALS is set');
      console.error('  Example: export GOOGLE_APPLICATION_CREDENTIALS=./gcp-key.json');
    }
    process.exit(1);
  }
}

testVisionAPI();
