<script context="module">
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	const API = PUBLIC_BACKEND_URL;
</script>

<script lang="ts">
	import '../../../app.css';
	import Heading from '../../../elements/Heading.svelte';
	import { AbstractionLevel } from '../../../types';
	import Dropdown from '../../../elements/Dropdown.svelte';
	import SummaryContainer from '../../../components/SummaryContainer.svelte';

	export let data;

	let abstractionLevel = AbstractionLevel.BOOK;
	let fileInput: HTMLInputElement;
	let isUploading = false;
	let uploadError = '';
	let style: string;
	let isChangingCharacter = false;
	let characterName = '';
	let characterDescription = '';
	let characters: { name: string; description: string }[] = [];
	let readingMode = false;

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
	}

	function selectCharacter(index: number) {
		// Select a character for modification
		const selectedCharacter = characters[index];
		characterName = selectedCharacter.name;
		characterDescription = selectedCharacter.description;
		isChangingCharacter = true;
	}

	async function handleFileUpload(event: Event) {
		const target = event.target as HTMLInputElement;

		if (!target?.files || target.files.length === 0) {
			uploadError = 'Invalid file selected.';
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

<main class="overflow-hidden h-full m-4">
	<div class="flex flex-col h-full">
		<button on:click={() => fileInput.click()} disabled={isUploading}>
			{isUploading ? 'Generating...' : 'Upload file'}
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
		<Heading heading={data.metadata.title} />
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
		{#if !readingMode}
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
					<button class="mt-2" on:click={addCharacter}
						>{#if isChangingCharacter}
							Change Character
						{:else}
							Add Character
						{/if}</button
					>
				</div>

				{#if characters.length > 0}
					<div class="ml-4">
						<h3>Characters:</h3>
						<ul>
							{#each characters as character, index (character.name)}
								<li>
									<button on:click={() => selectCharacter(index)} class="border-none">
										{character.name}: {character.description}
									</button>
								</li>
							{/each}
						</ul>
					</div>
				{/if}
			</div>
		{/if}
		<SummaryContainer
			book={data.book.book}
			selectedBook={data.id}
			{abstractionLevel}
			{style}
			{characters}
			{readingMode}
		/>
	</div>
</main>
