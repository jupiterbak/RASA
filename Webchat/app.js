const express = require('express');
const app = express();
var cors = require('cors');
const port = 3000;

app.use(cors({origin: 'http://localhost:3000'}));
app.use(express.static('public'));
app.listen(port, () => console.log(`listening on port ${port}!`));