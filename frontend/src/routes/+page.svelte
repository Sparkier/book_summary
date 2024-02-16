<script context="module">
	import { PUBLIC_DEV_BASE_URL } from '$env/static/public';
	const API = PUBLIC_DEV_BASE_URL;
</script>

<script lang="ts">
	import '../app.css';
	import SummaryContainer from '../components/SummaryContainer.svelte';
	import Heading from '../elements/Heading.svelte';
	import { AbstractionLevel } from '../types';
	import { fetchBooks, fetchBook } from '../api';

	let selectedBook = 'Alices Adventures in Wonderland';

	let abstractionLevel = AbstractionLevel.BOOK;
	let fileInput: HTMLInputElement;
	let isGenerating = false;
	let uploadError = '';

	async function handleFileUpload(event: Event) {
		const target = event.target as HTMLInputElement;

		if (!target?.files || target.files.length === 0) {
			uploadError = 'Wrong file selected.';
			return;
		}

		const file = target.files[0];
		isGenerating = true;
		uploadError = '';

		const formData = new FormData();
		formData.append('file', file);

		try {
			const response = await fetch('${API}/api/upload_book', {
				method: 'POST',
				body: formData
			});

			if (!response.ok) {
				const data = await response.json();
				// Set the error message
				console.log(data.error);

				uploadError = data.error || 'Upload failed';
			} else {
				uploadError = 'An error occurred during upload';
			}
		} catch (error) {
			// Set the error message
			uploadError = 'An error occurred during upload';
		} finally {
			// Set isGenerating back to false after the upload is complete
			isGenerating = false;
		}
	}
</script>

<main class="overflow-hidden h-full">
	<div class="flex flex-col h-full">
		<button on:click={() => fileInput.click()} disabled={isGenerating}>
			{isGenerating ? 'Generating...' : 'Upload file'}
		</button>
		<input
			type="file"
			accept=".epub"
			style="display: none"
			bind:this={fileInput}
			on:change={handleFileUpload}
		/>
		{#await fetchBooks() then books}
			<select bind:value={selectedBook}>
				{#each books as book}
					<option value={book}>
						{book}
					</option>
				{/each}
			</select>
			{#await fetchBook(selectedBook)}
				Loading book.
			{:then book}
				<Heading heading={book['title']} />
				<div class="py-2">
					<div class="flex">
						<p class="pr-2">Abstraction Level:</p>
						<select bind:value={abstractionLevel}>
							{#each Object.values(AbstractionLevel) as abstractionLevel}
								<option value={abstractionLevel}>
									{abstractionLevel}
								</option>
							{/each}
						</select>
					</div>
				</div>
				<SummaryContainer {book} {selectedBook} {abstractionLevel} />
			{:catch}
				<p style="color: red;">{uploadError || 'Book could not be loaded.'}</p>
			{/await}
		{/await}
	</div>
</main>
