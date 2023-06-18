<script lang="ts">
	import { createEventDispatcher } from "svelte";

	const dispatch = createEventDispatcher();

	export let players: string[];
	export let host: boolean = true;
</script>

<div class="p-3 bg-blue-400 flex gap-3 grow flex-wrap">
	{#each players as player, idx}
		<div class="flex bg-blue-300 p-2 rounded-md text-xl">
			<div class="font-mono mr-3">
				{idx + 1}
			</div>
			<div>
				{player}
			</div>
		</div>
	{/each}
	{#if host}
		<p class="flex justify-center">
			<button
				class="bg-blue-500 p-2 inline rounded-lg hover:bg-blue-600 active:bg-blue-700"
				on:click={() => dispatch("start")}
			>
				Start
			</button>
		</p>
	{/if}
</div>
