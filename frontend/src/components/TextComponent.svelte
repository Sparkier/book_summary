<script lang="ts">
	export let text: string;
	export let readingMode: boolean;
</script>

<div class="flex items-center justify-center">
	{#if readingMode}
		<div class="text-xl font-serif leading-relaxed text-left text-gray-800 bg-gray-100 p-4 mr-4">
			{text}
		</div>
	{:else}
		<div />
	{/if}
</div>
