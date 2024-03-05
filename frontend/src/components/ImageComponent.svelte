<script context="module">
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	const API = PUBLIC_BACKEND_URL;
</script>

<script lang="ts">
	export let src: string;
	export let text: string;
	export let style: string;
	export let characters: { name: string; description: string }[];
	export let readingMode: boolean;

	let isGenerating = false;
	let errorMessage = '';
	let imageVersions = 0;
	let prompt: string;
	let userModifiedPrompt = false;

	function getVersionNumber(src: string) {
		const parts = src.split('/');
		const book = parts[3];

		let fetchUrl = '';

		if (src.includes('get_book_summary_image')) {
			const index = parseInt(parts[4]);
			fetchUrl = `${API}/api/get_num_book_summary_images/${book}/${index}`;
		} else if (src.includes('get_chapter_summary_image')) {
			const chapter = parseInt(parts[4]);
			const index = parseInt(parts[5]);
			fetchUrl = `${API}/api/get_num_chapter_summary_images/${book}/${chapter}/${index}`;
		} else if (src.includes('get_paragraph_summary_image')) {
			const chapter = parseInt(parts[4]);
			const paragraph = parseInt(parts[5]);
			fetchUrl = `${API}/api/get_num_paragraph_summary_images/${book}/${chapter}/${paragraph}`;
		} else if (src.includes('get_paragraph_image')) {
			const chapter = parseInt(parts[4]);
			const paragraph = parseInt(parts[5]);
			fetchUrl = `${API}/api/get_num_paragraph_images/${book}/${chapter}/${paragraph}`;
		} else {
			errorMessage = 'Unknown image type';
			return;
		}

		fetch(fetchUrl)
			.then((response) => response.json())
			.then((data) => {
				imageVersions = data.versions;
			})
			.catch((error) => {
				errorMessage = 'Error while loading version: ' + error;
			});
	}

	function handleImageError() {
		errorMessage = 'No Image available';
	}

	async function get_updated_prompt() {
		let charactersInText: { name: string; description: string }[] = [];

		// Extract characters from the text
		characters.forEach((char) => {
			if (text.includes(char.name)) {
				charactersInText.push({ name: char.name, description: char.description });
			}
		});

		const characterText =
			charactersInText.length > 0
				? charactersInText.length === 1
					? `The character is ${charactersInText[0].name}, ${charactersInText[0].description}.`
					: `The characters are ${charactersInText
							.map((char) => `${char.name}, ${char.description}`)
							.join(' and ')}.`
				: '';

		let styleText = '';

		if (style !== 'No style') {
			styleText = `Generate an image in ${style} style.`;
		}

		const fullText = `${styleText} ${characterText} The scene is: ${text}`;
		prompt = fullText;
		return fullText;
	}

	async function generateImage() {
		//clear old error messages
		errorMessage = '';
		isGenerating = true;
		get_updated_prompt();

		try {
			const response = await fetch(`${API}/api/generate_image`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},

				body: JSON.stringify({ src, prompt })
			});

			if (response.ok) {
				getVersionNumber(src);
				isGenerating = false;
			} else {
				const responseData = await response.json();
				errorMessage = responseData.error || 'Error generating image';
			}
		} catch (error) {
			errorMessage = 'An unexpected error occurred while generating image';
		} finally {
			isGenerating = false;
		}
	}

	function updatePromptPeriodically() {
		if (!userModifiedPrompt) {
			get_updated_prompt();
		}
	}

	function handleTextareaInput(event: Event) {
		const target = event.target as HTMLTextAreaElement;
		userModifiedPrompt = true;
		prompt = target.value;
	}

	function resetUserModifiedPrompt() {
		userModifiedPrompt = false;
		get_updated_prompt();
	}

	setInterval(updatePromptPeriodically, 500);
	getVersionNumber(src);
	get_updated_prompt();
</script>

<div class="w-2/3">
	{#if readingMode}
		{#if imageVersions > 0}
			<div class="{readingMode ? '' : 'w-full overflow-x-scroll'}  flex">
				{#each [...Array(imageVersions)].map((_, index) => index) as version}
					<img
						src={`${src}${version > 0 ? `/${version}` : ''}`}
						alt="Summary of the text next to it."
						class="m-1 block max-w-48 max-h-48"
						on:error={() => handleImageError()}
					/>
				{/each}
			</div>
		{/if}
	{:else if imageVersions > 0}
		<div class="flex flex-col md:flex-row w-full">
			<div class="overflow-x-scroll flex max-w-49">
				{#each [...Array(imageVersions)].map((_, index) => index) as version}
					<img
						src={`${src}${version > 0 ? `/${version}` : ''}`}
						alt="Summary of the text next to it."
						class="m-1 block max-w-48 max-h-48"
						on:error={() => handleImageError()}
					/>
				{/each}
			</div>
			<div class="ml-4 flex flex-col w-full">
				<h3>Prompt:</h3>
				<textarea on:input={handleTextareaInput} rows="4" class="mt-2 w-full">{prompt}</textarea>
				<div class="flex mt-2">
					<div>
						{#if userModifiedPrompt}
							<button class="m-1" on:click={resetUserModifiedPrompt}>
								Reset to the generated prompt
							</button>
						{/if}
					</div>
					<div class="ml-auto">
						<button on:click={() => generateImage()} class="m-1">
							{isGenerating ? 'Generating...' : 'Generate a new image of the text'}
						</button>
						{#if errorMessage}
							<p class="text-red-600">{errorMessage}</p>
						{/if}
					</div>
				</div>
			</div>
		</div>
	{:else}
		<button on:click={() => generateImage()} class="m-1">
			{isGenerating ? 'Generating...' : 'Generate image of the text'}
		</button>
		{#if errorMessage}
			<p class="text-red-600">{errorMessage}</p>
		{/if}
	{/if}
</div>
