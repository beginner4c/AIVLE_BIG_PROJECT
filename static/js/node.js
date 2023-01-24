const express = require('express'); 
const app = express();
const path = require('path');
const http = require('http');
const server = http.createServer(app);

const socketIO = require('socket.io');
const io = socketIO(server);

app.use(express.static(path.join(__dirname, 'src')));

const PORT = process.env.PORT || 5000;

server.listen(PORT, () => {
  console.log(`server is running ${PORT}`);
});

io.on('connection', (socket) => {
  console.log('연결됨');
});