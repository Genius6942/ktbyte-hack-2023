<script lang="ts">
	export let question: string;
	export let answers: string[];

	import { createEventDispatcher } from "svelte";

	const dispatch = createEventDispatcher();
</script>

<div class="w-full h-1/2 text-center flex flex-col items-center">
	<p class="m-auto text-5xl px-10">{question}</p>
</div>
<hr />
<div class="w-full h-1/2 grid grid-cols-2 gap-4 p-4 text-base text-white">
	<button class="bg-blue-800 answer" on:click={() => dispatch('answer', {answer: answers[0]})} on:keydown={() => {}}>
		<p>{answers[0]}</p>
	</button>
	<button class="bg-blue-700 answer" on:click={() => dispatch('answer', {answer: answers[1]})} on:keydown={() => {}}>
		<p>{answers[1]}</p>
	</button>
	<button class="bg-blue-600 answer" on:click={() => dispatch('answer', {answer: answers[2]})} on:keydown={() => {}}>
		<p>{answers[2]}</p>
	</button>
	<button class="bg-blue-500 answer" on:click={() => dispatch('answer', {answer: answers[3]})} on:keydown={() => {}}>
		<p>{answers[3]}</p>
	</button>
</div>

<style>
	.answer {
		border-radius: 1rem;
		display: flex;
		align-items: center;
		flex-direction: column;
	}

	.answer > p {
		text-align: center;
		margin: auto;
	}
</style>
