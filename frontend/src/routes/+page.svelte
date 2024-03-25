<script context="module">
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	const API = PUBLIC_BACKEND_URL;
</script>

<script lang="ts">
	import '../app.css';
	import SummaryContainer from '../components/SummaryContainer.svelte';
	import Heading from '../elements/Heading.svelte';
	import { LibraryBig, Plus } from 'lucide-svelte';
	import { AbstractionLevel, ViewLevel } from '../types';
	import { fetchBooks, fetchBook } from '../api';
	import Dropdown from '../elements/Dropdown.svelte';

	let selectedBook = 'Alices Adventures in Wonderland';

	let abstractionLevel = AbstractionLevel.BOOK;
	let viewLevel = ViewLevel.IMAGE;
	let isUploading = false;
	let uploadError = '';
	let style: string;
	let isChangingCharacter = false;
	let characterName = '';
	let characterDescription = '';
	let characters: { name: string; description: string }[] = [];
	let readingMode = true;
	let addCharacterMode = false;

	function addCharacter() {
		const index = characters.findIndex((char) => char.name === characterName);

		if (index !== -1) {
			// Change character description if character exists
			characters[index].description = characterDescription;
		} else {
			// Add new character
			characters = [...characters, { name: characterName, description: characterDescription }];
		}
		// Clear input fields after adding/updating the character
		characterName = '';
		characterDescription = '';
		isChangingCharacter = false;
		addCharacterMode = false;
	}

	function selectCharacter(index: number) {
		// Select a character for modification
		addCharacterMode = true;
		const selectedCharacter = characters[index];
		characterName = selectedCharacter.name;
		characterDescription = selectedCharacter.description;
		isChangingCharacter = true;
	}

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

	function toggleReadingMode() {
		readingMode = !readingMode;
	}
	function toggleAddCharacterMode() {
		addCharacterMode = !addCharacterMode;
	}
</script>

<main class="overflow-hidden h-full">
	<div class="flex flex-col h-full">
		{#await fetchBooks() then books}
			{#await fetchBook(selectedBook)}
				Loading book.
			{:then book}
				<div class="py-2 flex items-start justify-between">
					<div class="ml-4 flex flex-col">
						<div class="flex items-center">
							<LibraryBig size={48} class="w-12 h-12 text-white bg-blue-500 rounded-lg p-2 mr-4 " />
							<p class="pr-2">Summarize:</p>
							<Dropdown items={Object.values(AbstractionLevel)} bind:value={abstractionLevel} />
							{#if readingMode}
								<p class="pr-2 pl-2">View:</p>
								<Dropdown items={Object.values(ViewLevel)} bind:value={viewLevel} />
							{/if}
							{#if !readingMode}
								<h3 class="pr-2 pl-2">Style:</h3>
								<select class="rounded border border-grey mt-3" bind:value={style}>
									<option value="anime">Anime</option>
									<option value="realistic">Realistic</option>
									<option value="cartoon">Cartoon</option>
									<option value="No style">No style</option>
								</select>
							{/if}
							<button
								on:click={() => toggleReadingMode()}
								class="absolute right-1 bg-blue-600 text-white rounded-lg px-6 py-2"
							>
								{readingMode ? 'Edit' : 'Back'}
							</button>
						</div>
						<Heading heading={book['title']} />
					</div>
				</div>

				{#if !readingMode}
					<div class="py-2 flex items-start ml-4">
						{#if characters.length > 0}
							<div class=" flex items-center">
								<ul class="flex list-none p-0">
									{#each characters as character, index (character.name)}
										<li class="mr-2">
											<button on:click={() => selectCharacter(index)} class="border-none">
												{character.name}
											</button>
										</li>
									{/each}
								</ul>
							</div>
						{/if}
						<!-- svelte-ignore a11y-click-events-have-key-events -->
						<div
							on:click={() => toggleAddCharacterMode()}
							class="ml-2 bg-blue-500 rounded-full w-10 h-10 flex items-center justify-center"
						>
							<Plus size={24} strokeWidth={1.25} />
						</div>
					</div>
					{#if addCharacterMode}
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
								style="width: 300px;"
							/>
							<button class="mt-2" on:click={addCharacter} style="width: 300px;">
								{#if isChangingCharacter}
									Change Character
								{:else}
									Add Character
								{/if}
							</button>
						</div>
					{/if}
				{/if}
				<SummaryContainer
					{book}
					{selectedBook}
					{abstractionLevel}
					{style}
					{characters}
					{readingMode}
					{viewLevel}
				/>
			{:catch}
				<p class="text-red-600">{'Book could not be loaded.'}</p>
			{/await}
		{/await}
	</div>
</main>
