<script lang="ts">
	export let title: string;
	export let creator: string;
	export let imageSrc: string;
</script>

<div
	class="flex flex-col border w-64 h-64 rounded-lg shadow-2xl"
	style="background: linear-gradient(to right, rgb(60, 13, 20) 3px, rgba(255, 255, 255, 0.5) 5px, rgba(255, 255, 255, 0.25) 7px, rgba(255, 255, 255, 0.25) 10px, transparent 12px, transparent 16px, rgba(255, 255, 255, 0.25) 17px, transparent 22px), url({imageSrc}), url({'EmptyImage.jpg'})"
>
	<div class="flex-1 flex flex-col justify-between p-2">
		<h3
			class="text-xl font-bold text-center tracking-tight text-gray-900 p-1 mx-4 rounded backdrop-blur"
		>
			{title}
		</h3>
		{#if creator}
			<p class="mb-4 text-sm font-medium text-center text-gray-600 p-1 backdrop-blur rounded">
				{creator}
			</p>
		{/if}
	</div>
</div>
