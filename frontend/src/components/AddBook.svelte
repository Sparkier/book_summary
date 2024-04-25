<script lang="ts">
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	import { Plus } from 'lucide-svelte';

	const API = PUBLIC_BACKEND_URL;
	let fileInput: HTMLInputElement;
	let isUploading = false;
	let uploadError = '';
	let fileName = '';

	async function handleFileUpload(event: Event) {
		const target = event.target as HTMLInputElement;

		if (!target?.files || target.files.length === 0) {
			uploadError = 'Wrong file selected.';
			return;
		}

		const file = target.files[0];
		fileName = file.name;
		isUploading = true;
		uploadError = '';

		const formData = new FormData();
		formData.append('file', file);

		try {
			const response = await fetch(`${API}/api/book`, {
				method: 'POST',
				body: formData
			});
			if (!response.ok) {
				const data = await response.json();
				uploadError = data.error || 'Upload failed';
				isUploading = false;
			} else {
				isUploading = true;
			}
		} catch (error) {
			uploadError = 'An error occurred during upload';
			isUploading = false;
		}
	}
</script>

<div class="flex items-center justify-center">
	{#if !isUploading}
		<button
			on:click={() => fileInput.click()}
			class="bg-blue-500 p-2 rounded-lg text-white flex items-center justify-center gap-2"
		>
			<Plus />
		</button>
	{:else}
		<div>Uploading Book</div>
	{/if}
</div>
{#if uploadError}
	<p class="text-red-600">{uploadError}</p>
{/if}

<input
	type="file"
	accept=".epub"
	style="display: none"
	bind:this={fileInput}
	on:change={handleFileUpload}
/>
