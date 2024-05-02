<script lang="ts">
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	import { Plus } from 'lucide-svelte';

	const API = PUBLIC_BACKEND_URL;
	let fileInput: HTMLInputElement;
	let isUploading = false;
	let uploadError = '';
	let progressError = '';
	let fileName = '';
	let progress = 0;

	async function handleFileUpload(event: Event) {
		const target = event.target as HTMLInputElement;

		if (!target?.files || target.files.length === 0) {
			uploadError = 'Wrong file selected.';
			return;
		}

		const file = target.files[0];
		fileName = file.name;
		uploadError = '';
		pollProgress();
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
			}
		} catch (error) {
			uploadError = 'An error occurred during upload';
			isUploading = false;
		}
	}
	async function initial() {
		const response = await fetch(`${API}/api/book/progress`);
		const data = await response.json();
		if (data.progress != 0) {
			pollProgress();
		}
	}

	async function pollProgress() {
		isUploading = true;
		try {
			const response = await fetch(`${API}/api/book/progress`);
			const data = await response.json();
			progress = data.progress;
			if (progress < 100) {
				// If progress is not complete and uploading is still in progress, continue polling
				setTimeout(pollProgress, 5000);
			} else {
				isUploading = false;
			}
		} catch (error) {
			progressError = 'Error fetching progress:';
		}
	}
	initial();
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
		<div class="w-full bg-gray-200 rounded-lg mt-1" style="width:300px">
			<div
				class="bg-blue-500 text-xs leading-none py-1 text-center text-white rounded-lg"
				style="width: {Math.floor(progress)}%"
			>
				{Math.floor(progress)}%
				{#if progressError}
					<p class="text-red-600">{progressError}</p>
				{/if}
			</div>
		</div>
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
