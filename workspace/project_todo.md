[ ] Use `list_files` to check for existing environment/dependency files.
[ ] Use `install_package` to install 'axios'.
[ ] Use `write_file` to create 'fetchObjects.js' with the following content:
[ ] ```javascript
[ ] const axios = require('axios');
[ ] async function fetchObjects() {
[ ] try {
[ ] get('https://api.restful-api.dev/objects');
[ ] log(JSON.stringify(response.data, null, 2));
[ ] } catch (error) {
[ ] error('Error fetching objects:', error);
[ ] }
[ ] }
[ ] fetchObjects();
[ ] ```
[ ] Use `run_code` to execute 'fetchObjects.js'.
[ ] Use `read_output` to verify the output is structured and matches expectations.