<script lang="ts">
	import '../app.css';
	import SummaryContainer from '../components/SummaryContainer.svelte';
	import Heading from '../elements/Heading.svelte';
	import { LibraryBig, Plus, Trash2 } from 'lucide-svelte';
	import { AbstractionLevel, ViewMode } from '../types';
	import { fetchBook } from '../api';
	import Dropdown from '../elements/Dropdown.svelte';
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	const API = PUBLIC_BACKEND_URL;

	let selectedBook = 'Alices Adventures in Wonderland';

	let abstractionLevel = AbstractionLevel.BOOK;
	let viewMode = ViewMode.IMAGE;
	let style: string;
	let isChangingCharacter = false;
	let characterName = '';
	let characterDescription = '';
	let characterId = NaN;
	let characters: { name: string; description: string; id: number }[] = [];
	let characterIdCounter = 0;
	let readingMode = true;
	let addCharacterMode = false;
	let errorMessage = '';

	async function addCharacter() {
		const index = characters.findIndex((char) => char.id === characterId);

		if (index !== -1) {
			// Change character description if character exists
			characters[index].name = characterName;
			characters[index].description = characterDescription;
		} else {
			// Add new character
			characters = [
				...characters,
				{ name: characterName, description: characterDescription, id: characterIdCounter }
			];
			characterIdCounter++;
		}
		saveCharacters();
	}

	async function loadCharacters() {
		try {
			const response = await fetch(`${API}/api/books/${selectedBook}/characters`);
			const data = await response.json();
			characters = data;
			// Get a correct ID counter again
			let maxId = 0;
			characters.forEach((character) => {
				if (character.id > maxId) {
					maxId = character.id;
				}
			});

			characterIdCounter = maxId + 1;
		} catch (error) {
			errorMessage = 'Error loading characters:' + error;
		}
	}

	async function saveCharacters() {
		try {
			const response = await fetch(`${API}/api/books/${selectedBook}/characters`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(characters)
			});

			if (response.ok) {
				// Clear input fields after adding/updating the character
				characterName = '';
				characterDescription = '';
				characterId = NaN;
				isChangingCharacter = false;
				addCharacterMode = false;
			} else {
				errorMessage = 'Error saving characters:' + response.statusText;
			}
		} catch (error) {
			errorMessage = 'Error saving characters:';
		}
	}

	function selectCharacter(index: number) {
		// Select a character for modification
		addCharacterMode = true;
		const selectedCharacter = characters[index];
		characterId = selectedCharacter.id;
		characterName = selectedCharacter.name;
		characterDescription = selectedCharacter.description;
		isChangingCharacter = true;
	}

	function deleteCharacter(id: number) {
		characters = characters.filter((char) => char.id !== id);
		saveCharacters();
	}

	function toggleReadingMode() {
		readingMode = !readingMode;
	}

	function toggleAddCharacterMode() {
		addCharacterMode = !addCharacterMode;
	}

	loadCharacters();
</script>

<main class="overflow-hidden h-full">
	<div class="flex flex-col h-full">
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
							<Dropdown items={Object.values(ViewMode)} bind:value={viewMode} />
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
							{readingMode ? 'Edit' : 'View'}
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
								{#each characters as character, index (character.id)}
									<li class="mr-2">
										<div class="flex items-center rounded-xl border-none bg-slate-100">
											<button on:click={() => selectCharacter(index)} class="border-none mt-1">
												{character.name}
											</button>
											<!-- svelte-ignore a11y-click-events-have-key-events -->
											<div
												on:click={() => deleteCharacter(character.id)}
												class="rounded-full w-4 h-4 flex items-center justify-center mr-2"
											>
												<Trash2 />
											</div>
										</div>
									</li>
								{/each}
							</ul>
						</div>
					{/if}
					<!-- svelte-ignore a11y-click-events-have-key-events -->
					<div
						on:click={() => toggleAddCharacterMode()}
						class="ml-2 mt-1 bg-blue-500 rounded-full w-10 h-10 flex items-center justify-center"
					>
						<Plus size={24} strokeWidth={1.25} />
					</div>
					{#if errorMessage}
						<p class="text-red-600">{errorMessage}</p>
					{/if}
				</div>
				{#if addCharacterMode}
					<div class="ml-4 flex flex-col">
						<h3>Name:</h3>
						<div class="flex items-center">
							<input
								class="common-input"
								bind:value={characterName}
								type="text"
								placeholder="Alice"
								style="width: 300px;"
							/>
						</div>
						<h3>Description:</h3>
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
				{viewMode}
			/>
		{:catch}
			<p class="text-red-600">{'Book could not be loaded.'}</p>
		{/await}
	</div>
</main>
