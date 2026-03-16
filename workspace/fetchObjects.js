const axios = require('axios');
async function fetchObjects() {
  try {
    const response = await axios.get('https://api.restful-api.dev/objects');
    console.log(JSON.stringify(response.data, null, 2));
  } catch (error) {
    console.error('Error fetching objects:', error);
  }
}
fetchObjects();