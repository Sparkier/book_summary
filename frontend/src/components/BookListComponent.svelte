<script lang="ts">
	import BookCard from '../elements/BookCard.svelte';
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	const API = PUBLIC_BACKEND_URL;

	export let books: { uuid: string; title: string; creator: string }[];

	let fileInput: HTMLInputElement;
	let isUploading = false;
	let uploadError = '';

	async function handleFileUpload(event: Event) {
		const target = event.target as HTMLInputElement;

		if (!target?.files || target.files.length === 0) {
			uploadError = 'Wrong file selected.';
			return;
		}

		const file = target.files[0];
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

<div class="mx-auto">
	<div class="flex flex-wrap justify-start gap-4 m-3">
		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<div on:click={() => fileInput.click()}>
			{#if !isUploading}
				<a href="http://localhost:5173/#">
					<BookCard title="Add book" imageSrc="EmptyImage.jpg" creator="" />
				</a>
			{:else}
				<a href="http://localhost:5173/#">
					<BookCard title="Uploading..." imageSrc="EmptyImage.jpg" creator="" />
				</a>
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
		</div>
		{#each books as book (book.uuid)}
			<a href="/book/{book.uuid}">
				<BookCard
					title={book.title}
					imageSrc={`/api/books/${book.uuid}/images/0`}
					creator={book.creator}
				/>
			</a>
		{/each}
	</div>
</div>
