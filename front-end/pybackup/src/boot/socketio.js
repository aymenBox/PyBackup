import { boot } from 'quasar/wrappers';
import { io } from 'socket.io-client';

const socketio = io('http://127.0.0.1:8088');
socketio.on('connect', () => {
    console.log('Connected to the server from socketio.js'); 
})
const socketioVersion = io.socketioVersion;

console.log('Socket.IO version:', socketioVersion);
export default boot(({ app }) => {
  // Inject the socketio instance into the app
  app.config.globalProperties.$socketio = socketio;
});

export{socketio};
