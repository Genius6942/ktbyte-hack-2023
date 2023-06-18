<script lang="ts">
	interface PlayerData {
		name: string;
		score: number;
	}
	export let end: boolean = false;
	export let players: PlayerData[];
</script>

<div class="p-3 bg-blue-100 flex flex-col gap-3 grow h-full">
	{#if end}
		Game over.
	{/if}
	{#each players as player, idx}
		<div class="flex bg-blue-300 p-2 rounded-md text-xl">
			<div class="font-mono mr-3">
				{idx + 1}
			</div>
			<div>
				{player.name}
			</div>
			<div class="ml-auto mr-3 flex items-center gap-1">
				Score:
				<div class="font-mono">
					{player.score}
				</div>
			</div>
		</div>
	{/each}
</div>
