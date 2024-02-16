<script lang="ts">
	export let src: string;
	export let text: string;
	let isImageAvailable = true;
	let isGenerating = false;

	function handleImageError() {
		console.error('No Image available');
		isImageAvailable = false;
	}

	async function generateImage() {
		isGenerating = true;
		try {
			const response = await fetch('http://127.0.0.1:5000/api/generate_image', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ src, text })
			});

			if (response.ok) {
				isGenerating = false;
			} else {
				console.error('Error sending to the server:', response.statusText);
			}
		} catch (error) {
			console.error('Error sending to the server:', error);
		}
	}
</script>

<div>
	{#if isImageAvailable}
		<img
			{src}
			alt="Summary of the text next to it."
			class={`m-1 w-48`}
			on:error={() => handleImageError()}
		/>
		<button on:click={() => generateImage()} class="m-1 w-48">
			{isGenerating ? 'Generating...' : 'Generate a new image of the text'}</button
		>
	{:else}
		<button on:click={() => generateImage()} class="m-1 w-48">
			{isGenerating ? 'Generating...' : 'Generate image of the text'}</button
		>
	{/if}
</div>
