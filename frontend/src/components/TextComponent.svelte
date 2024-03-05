<script lang="ts">
	export let text: string;
	export let readingMode: boolean;
</script>

<div class="{readingMode ? 'w-1/2' : 'w-1/3'} border-r-4 flex items-center justify-center">
	{#if readingMode}
		<div class="text-xl font-serif leading-relaxed text-left text-gray-800 bg-gray-100 p-4 mr-4">
			{text}
		</div>
	{:else}
		<div>
			{text}
		</div>
	{/if}
</div>
