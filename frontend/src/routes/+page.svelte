<script lang="ts">
	import '../app.css';
	import SummaryContainer from '../components/SummaryContainer.svelte';
	import Heading from '../elements/Heading.svelte';
	import { AbstractionLevel } from '../types';
	import { fetchBooks, fetchBook } from '../api';

	let selectedBook = 'Alices Adventures in Wonderland';

	let abstractionLevel = AbstractionLevel.BOOK;
	let fileInput: any;
	let isGenerating = false;

	async function handleFileUpload(event: any) {
		const file = event.target.files[0];
		console.log('Hochgeladene .epub-Datei:', file);

		// Set isGenerating to true before uploading the book
		isGenerating = true;

		const formData = new FormData();
		formData.append('file', file);

		try {
			const response = await fetch('http://127.0.0.1:5000/api/upload_book', {
				method: 'POST',
				body: formData
			});

			if (response.ok) {
				const data = await response.json();
				console.log('Erfolgreich hochgeladen:', data);
				// Reload the page after successful generation
				location.reload();
			} else {
				console.error('Fehler beim Hochladen:', response.statusText);
			}
		} catch (error) {
			console.error('Fehler beim Hochladen:', error);
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
				Book could not be loaded.
			{/await}
		{/await}
	</div>
</main>
