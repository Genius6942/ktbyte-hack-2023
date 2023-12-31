import { io } from 'socket.io-client';

export const socket = io(import.meta.env.DEV ? 'http://localhost:8080' : 'https://ktbyte-hack-2023.smart09codes.repl.co', {transports: ['websocket']});

export const init = (name: string) => {
	socket.emit('init', { name });
	console.log('starting up ' + name);
};

export function joinRoom(roomId: string) {
	socket.emit('join', { room: roomId });
}

export function create(topic: string) {
	socket.emit('create', {topic});
}

export function sendAnswer(answer: number) {
	socket.emit('answer', { answer });
}

socket.on('server-error', ({message}) => {
	try {
	console.error(message);
	typeof alert !== 'undefined' && alert(message);
	} catch (e) {
		console.error(e);
	}
});