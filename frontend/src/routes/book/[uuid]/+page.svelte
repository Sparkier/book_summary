<script lang="ts">
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	import { fetchBook } from '$lib/api';
	import SummaryContainer from '$lib/components/SummaryContainer.svelte';
	import Dropdown from '$lib/elements/Dropdown.svelte';
	import Button from '$lib/elements/Button.svelte';
	import { AbstractionLevel, ViewMode } from '$lib/types';
	import { LibraryBig, Plus, Trash2 } from 'lucide-svelte';
	const API = PUBLIC_BACKEND_URL;

	const url = window.location.pathname;
	const urlParts = url.split('/');
	const uuid = urlParts[urlParts.length - 2];
	let selectedBook = uuid;

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

	function handleKeyDown(event: { which: number }) {
		if (event.which == 13) {
			addCharacter();
		}
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
						<a href="/">
							<LibraryBig size={48} class="w-12 h-12 text-white bg-blue-500 rounded-lg p-2 mr-4 " />
						</a>
						<p class="pr-2 pl-2">Summarize:</p>
						<Dropdown items={Object.values(AbstractionLevel)} bind:value={abstractionLevel} />
						{#if readingMode}
							<p class="pr-2 pl-2">View:</p>
							<Dropdown items={Object.values(ViewMode)} bind:value={viewMode} />
						{/if}
						{#if !readingMode}
							<p class="pr-2 pl-2">Style:</p>
							<select class="rounded border border-grey" bind:value={style}>
								<option value="anime">Anime</option>
								<option value="realistic">Realistic</option>
								<option value="cartoon">Cartoon</option>
								<option value="No style">No style</option>
							</select>
						{/if}
						<Button
							on:click={() => toggleReadingMode()}
							classNames="absolute right-1 bg-blue-600 text-white rounded-lg px-6 py-2 mr-2"
						>
							{readingMode ? 'Edit' : 'View'}
						</Button>
					</div>
					<h2>{book['title']}</h2>
				</div>
			</div>

			{#if !readingMode}
				<div class="py-2 flex items-start ml-4">
					{#if characters.length > 0}
						<div class=" flex items-center">
							<ul class="flex list-none p-0">
								{#each characters as character, index (character.id)}
									<li class="mr-2">
										<div class="flex items-center rounded-xl border-none bg-slate-100 p-2">
											<button on:click={() => selectCharacter(index)} class="border-none mr-1">
												{character.name}
											</button>
											<!-- svelte-ignore a11y-click-events-have-key-events -->
											<div
												on:click={() => deleteCharacter(character.id)}
												class="rounded-full w-4 h-4 flex items-center justify-center"
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
					<div class="ml-4 flex flex-col mb-2" style="width: 300px;">
						<h4>Name:</h4>
						<div class="flex items-center">
							<input
								class="common-input border mt-1"
								bind:value={characterName}
								type="text"
								placeholder="Alice"
							/>
						</div>
						<h4>Description:</h4>
						<textarea
							class="common-input mt-1 border"
							bind:value={characterDescription}
							placeholder="a blond girl in a blue dress"
							rows="3"
							on:keydown={handleKeyDown}
						/>
						<Button on:click={addCharacter} classNames="mt-2">
							{#if isChangingCharacter}
								Change Character
							{:else}
								Add Character
							{/if}
						</Button>
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
