<script context="module">
	import { PUBLIC_DEV_BASE_URL } from '$env/static/public';
	const API = PUBLIC_DEV_BASE_URL;
</script>

<script lang="ts">
	export let src: string;
	export let text: string;
	let isImageAvailable = true;
	let isGenerating = false;
	let errorMessage = '';

	function handleImageError() {
		isImageAvailable = false;
	}

	async function generateImage() {
		//clear old error messages
		errorMessage = '';
		isGenerating = true;
		try {
			const response = await fetch(`${API}/api/generate_image`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ src, text })
			});

			if (response.ok) {
				isGenerating = false;
			} else {
				const responseData = await response.json();
				errorMessage = responseData.error || 'Error generating image';
			}
		} catch (error) {
			errorMessage = 'An unexpected error occurred while generating image';
		} finally {
			isGenerating = false;
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
			{isGenerating ? 'Generating...' : 'Generate a new image of the text'}
		</button>
		{#if errorMessage}
			<p class="text-red-600">{errorMessage}</p>
		{/if}
	{:else}
		<button on:click={() => generateImage()} class="m-1 w-48">
			{isGenerating ? 'Generating...' : 'Generate image of the text'}
		</button>
	{/if}
</div>
