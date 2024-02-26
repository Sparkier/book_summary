<script context="module">
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	const API = PUBLIC_BACKEND_URL;
</script>

<script lang="ts">
	import '../app.css';
	import SummaryContainer from '../components/SummaryContainer.svelte';
	import Heading from '../elements/Heading.svelte';
	import { AbstractionLevel } from '../types';
	import { fetchBooks, fetchBook } from '../api';
	import Dropdown from '../elements/Dropdown.svelte';

	let selectedBook = 'Alices Adventures in Wonderland';

	let abstractionLevel = AbstractionLevel.BOOK;
	let fileInput: HTMLInputElement;
	let isGenerating = false;
	let uploadError = '';
	let style: string;
	let characterName = '';
	let characterDescription = '';
	let characters: { name: string; description: string }[] = [];
	let readingMode = false;

	const SERVER_IP = '127.0.0.1';
	const SERVER_PORT = '5000';

	function saveCharactersToStorage() {
		localStorage.setItem('characters', JSON.stringify(characters));
	}
	function addCharacter() {
		characters = [...characters, { name: characterName, description: characterDescription }];
		saveCharactersToStorage();
		// Clear input fields after adding the character
		characterName = '';
		characterDescription = '';
	}

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
			const response = await fetch(`${API}/api/upload_book`, {
				method: 'POST',
				body: formData
			});
			if (!response.ok) {
				const data = await response.json();
				uploadError = data.error || 'Upload failed';
			} else {
				isGenerating = true;
			}
		} catch (error) {
			uploadError = 'An error occurred during upload';
		} finally {
			isGenerating = false;
		}
	}
</script>

<main class="overflow-hidden h-full m-4">
	<div class="flex flex-col h-full">
		<button on:click={() => fileInput.click()} disabled={isGenerating}>
			{isGenerating ? 'Generating...' : 'Upload file'}
		</button>
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

				{#if readingMode}
					<div class="py-2 flex items-start">
						<div class="ml-4 flex flex-col">
							<div class="flex items-center">
								<p class="pr-2">Abstraction Level:</p>
								<Dropdown items={Object.values(AbstractionLevel)} bind:value={abstractionLevel} />

								<h3 class="ml-2 mr-2">Style:</h3>
								<select bind:value={style}>
									<option value="anime">Anime</option>
									<option value="realistic">Realistic</option>
									<option value="cartoon">Cartoon</option>
									<option value="No style">No style</option>
								</select>
								<label for="readingMode" class="ml-2 mr-2">Reading Mode</label>
								<input type="checkbox" bind:checked={readingMode} id="readingMode" />
							</div>
						</div>
					</div>
				{:else}
					<div class="py-2 flex items-start">
						<div class="ml-4 flex flex-col">
							<div class="flex items-center">
								<p class="pr-2">Abstraction Level:</p>
								<Dropdown items={Object.values(AbstractionLevel)} bind:value={abstractionLevel} />

								<h3 class="ml-2 mr-2">Style:</h3>
								<select bind:value={style}>
									<option value="anime">Anime</option>
									<option value="realistic">Realistic</option>
									<option value="cartoon">Cartoon</option>
									<option value="No style">No style</option>
								</select>
								<label for="readingMode" class="ml-2 mr-2">Reading Mode</label>
								<input type="checkbox" bind:checked={readingMode} id="readingModeID" />
							</div>
						</div>
					</div>

					<div class="py-2 flex items-start">
						<div class="ml-4 flex flex-col">
							<h3>Character Name:</h3>
							<div class="flex items-center">
								<input
									class="common-input"
									bind:value={characterName}
									type="text"
									placeholder="Alice"
									style="width: 300px;"
								/>
							</div>
							<h3>Character Description:</h3>
							<textarea
								class="common-input mt-2"
								bind:value={characterDescription}
								placeholder="a blond girl in a blue dress"
								rows="3"
							/>
							<button class="mt-2" on:click={addCharacter}>Add Character</button>
						</div>

						{#if characters.length > 0}
							<div class="ml-4">
								<h3>Added Characters:</h3>
								<ul>
									{#each characters as character (character.name)}
										<li>{character.name}: {character.description}</li>
									{/each}
								</ul>
							</div>
						{/if}
					</div>
				{/if}
				<SummaryContainer
					{book}
					{selectedBook}
					{abstractionLevel}
					{style}
					{characters}
					{readingMode}
				/>
			{:catch}
				<p class="text-red-600">{'Book could not be loaded.'}</p>
			{/await}
		{/await}
	</div>
</main>
