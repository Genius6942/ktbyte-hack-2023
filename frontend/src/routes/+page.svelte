<script lang="ts">
	import { init, joinRoom, create, socket } from "../lib/socket";
	// import audioSrc from "../background_music.mp3";
	import { onMount, onDestroy } from "svelte";
	import Leaderboard from "./leaderboard.svelte";
	import Question from "./question.svelte";
	// @ts-ignore
	import { Howl, Howler } from "howler";
	import "../app.css";
	import Begin from "./begin.svelte";

	interface Question {
		question: string;
		possibleAnswers: string[];
	}
	interface PlayerData {
		name: string;
		id: string;
		score: number;
	}

	let question = "";
	let answers: string[] = [];
	let name = "";
	let roomId = "";
	let roomTopic = "";
	let players: PlayerData[] = [];
	let host = false;
	let correctAnswer = "";
	let end = false;

	socket.on("state", ({ players: updatedPlayers }: { players: PlayerData[] }) => {
		console.log(players)
		players = updatedPlayers.sort((a, b) => b.score - a.score);
	});
	socket.on("question", (qa: { question: string; answers: string[] }) => {
		question = qa.question;
		answers = qa.answers;
		state = 3;
	});
	socket.on("end", () => {
		end = true;
	});

	socket.on("roomId", ({ id }: { id: string }) => {
		roomId = id;
		state = Math.max(state, 2);
	});
	socket.on("generateQuestion", () => {
		state = 2.25;
	});
	socket.on("generateAnswers", ({ question: newQuestion }: { question: string }) => {
		question = newQuestion;
		state = 2.5;
	});
	socket.on("leaderboard", () => {
		state = 5;
	});
	socket.on("answer", ({ answer: finalAnswer }: { answer: string }) => {
		correctAnswer = finalAnswer;
		state = 4;
	});
	socket.on("topic", ({ topic }: { topic: string }) => {
		roomTopic = topic;
	});

	// socket.on("server-error", ({ message }: { message: string }) => {
	// 	alert("Error: " + message);
	// });

	let state = 0;
	let sound: Howl;

	onMount(() => {
		let background_music = new Audio("/Quiz BACKGROUND MUSIC.mp3");
		background_music.loop = true;
	});

	let id = "";
	socket.on("connect", () => {
		id = socket.id;
	});

	onDestroy(() => {
		if (sound) {
			// sound.stop(); // Stop the background music when the component is unmounted
		}
	});
</script>

<div
	class="flex items-center justify-center h-screen bg-blue-100"
	style="display: {state == 0 ? 'flex' : 'none'}"
>
	<div class="p-5 rounded-xl bg-blue-200 flex flex-col items-center">
		<p class="text-5xl mb-4">Welcome to QuizAI!</p>
		<div class="flex items-center justify-center gap-3">
			<input
				class="bg-blue-100 p-2 rounded-xl focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-opacity-50"
				type="text"
				bind:value={name}
				on:keydown={({ key }) => {
					if (key === "Enter") {
						if (name.length === 0) {
							return;
						}
						state++;
						init(name);
					}
					sound.play();
				}}
				placeholder="Enter Your Name"
				maxlength={15}
			/>
			<button
				class="border-4 border-blue-500 p-2 rounded-xl hover:bg-blue-500 hover:text-white transition-all"
				on:click={() => {
					if (name.length === 0) {
						return;
					}
					state++;
					init(name);
					sound.play();
				}}
			>
				Next
			</button>
		</div>
	</div>
</div>

<div
	class="flex items-center justify-center h-screen flex-col bg-blue-100"
	style="display: {state == 1 ? 'flex' : 'none'}"
>
	<h1 class="text-5xl mb-10">Join or create a room!</h1>
	<div class="flex items-center relative gap-2">
		<div class="flex flex-col items-center rounded-xl p-3 bg-blue-200 gap-3">
			<input
				type="text"
				class="bg-blue-100 p-2 rounded-xl mb-3 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-opacity-50"
				bind:value={roomId}
				placeholder="Enter Room Code"
			/>
			<button
				class="border-4 border-blue-500 p-2 rounded-xl hover:bg-blue-500 hover:text-white transition-all"
				on:click={() => joinRoom(roomId)}
			>
				Join Room
			</button>
		</div>
		<div class="h-full w-1 bg-black" />
		<div class="flex flex-col items-center justify-center rounded-xl p-3 bg-blue-200 gap-3 h-full">
			<input
				type="text"
				class="bg-blue-100 p-2 rounded-xl mb-3 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-opacity-50"
				bind:value={roomTopic}
				placeholder="Enter Room Topic"
			/>
			<button
				class="border-4 border-blue-500 p-2 rounded-xl hover:bg-blue-500 hover:text-white transition-all"
				on:click={() => {
					create(roomTopic);
					host = true;
				}}
			>
				Create Room
			</button>
		</div>
	</div>
</div>

<!-- Game view -->

<div class="w-screen h-screen flex flex-col" style={`display: ${state >= 2 ? "flex" : "none"}`}>
	<div class="flex bg-blue-700 text-white p-2 font-2xl">
		Room code: {roomId}
		<button
			class="ml-auto ml-3 bg-blue-700 text-white px-2 font-2xl bg-blue-500 py-1 rounded-md"
			on:click={() => history.go(0)}
		>
			Leave
		</button>
	</div>
	<div class="grow bg-blue-300 relative">
		{#if state === 2}
			<Begin
				players={players.map((player) => player.name)}
				on:start={() => socket.emit("start")}
				{host}
			/>
		{:else if state === 2.25}
			<div class="h-full text-6xl text-white flex items-center justify-center">
				Generating question...
			</div>
		{:else if state === 2.5}
			<div class="h-full text-4xl text-white flex items-center justify-center">
				<div>
				Question: {question}
				<br />
				Generating answers...</div>
			</div>
		{:else if state === 3}
			<Question
				{question}
				{answers}
				on:answer={(e) => {
					socket.emit("answer", { answer: e.detail.answer });
					state = 3.5;
				}}
			/>
		{:else if state === 3.5}
			You submitted your answer. Waiting...
		{:else if state === 4}
			The answer was: {correctAnswer}
		{:else if state === 5}
			<Leaderboard {players} end={end}/>
		{/if}
	</div>
	<div class="bg-blue-700 flex p-2 text-white">
		Topic: {roomTopic}
		<div class="ml-auto mr-3">
			Score: {players.find((player) => player.id === socket.id)?.score ?? 0}{" "}Rank: {Math.max(
				players.findIndex((player) => player.id === id),
				0
			) + 1}
		</div>
	</div>
</div>
