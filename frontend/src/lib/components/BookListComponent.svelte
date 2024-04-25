<script lang="ts">
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	import BookCard from '$lib/elements/BookCard.svelte';

	export let books: { uuid: string; title: string; creator: string }[];

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

<div class="flex flex-wrap justify-start gap-4">
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	{#if !isUploading}
		<div on:click={() => fileInput.click()}>
			<BookCard
				title="New Book"
				imageSrc="EmptyImage.jpg"
				creator=""
				button={true}
				buttonMsg="Add"
				btnDisabled={false}
			/>
		</div>
	{:else}
		<BookCard
			title={fileName}
			imageSrc="EmptyImage.jpg"
			creator=""
			button={true}
			buttonMsg="Uploading..."
			btnDisabled={true}
		/>
	{/if}
	<input
		type="file"
		accept=".epub"
		style="display: none"
		bind:this={fileInput}
		on:change={handleFileUpload}
	/>
	{#if uploadError}
		<p class="text-red-600">{uploadError}</p>
	{/if}

	{#each books as book (book.uuid)}
		<a href="/book/{book.uuid}">
			<BookCard
				title={book.title}
				imageSrc={`/api/books/${book.uuid}/images/0`}
				creator={book.creator}
				button={false}
				buttonMsg=""
				btnDisabled={true}
			/>
		</a>
	{/each}
</div>
