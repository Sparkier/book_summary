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
	let selectedImageIndex = 0;

	function getVersionNumber(src: string) {
		const parts = src.split('/');
		const book = parts[3];

		let fetchUrl = '';

		if (src.includes('/images')) {
			fetchUrl = `${API}/api/books/${book}/image/versions`;
		}
		if (src.includes('/chapters')) {
			const chapter = parseInt(parts[5]);
			fetchUrl = `${API}/api/books/${book}/chapters/${chapter}/image/versions`;
		}
		if (src.includes('/summarized_paragraphs')) {
			const chapter = parseInt(parts[5]);
			const paragraph = parseInt(parts[7]);
			fetchUrl = `${API}/api/books/${book}/chapters/${chapter}/summarized_paragraphs/${paragraph}/image/versions`;
		}
		if (src.includes('/paragraphs')) {
			const chapter = parseInt(parts[5]);
			const paragraph = parseInt(parts[7]);
			fetchUrl = `${API}/api/books/${book}/chapters/${chapter}/paragraphs/${paragraph}/image/versions`;
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
			const response = await fetch(`${API}/api/image`, {
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

	function setSelectedImage(index: number) {
		selectedImageIndex = index;
	}

	setInterval(updatePromptPeriodically, 500);
	getVersionNumber(src);
	get_updated_prompt();
</script>

<div class="w-full">
	{#if readingMode}
		<div class=" w-64 h-64 flex flex-wrap">
			<img
				src={`${src}/${selectedImageIndex}`}
				alt="Summary of the text next to it."
				class="block w-64 h-64"
				on:error={() => handleImageError()}
			/>
		</div>
	{:else if imageVersions > 0}
		<div class="flex flex-col md:flex-row w-full">
			<img
				src={`${src}/${selectedImageIndex}`}
				alt="Summary of the text next to it."
				class="block w-64 h-64"
				on:error={() => handleImageError()}
			/>

			<div class="ml-4 flex flex-col w-full">
				<div class="overflow-x-auto max-h-24 flex">
					{#each [...Array(imageVersions)].map((_, index) => index) as version}
						<!-- svelte-ignore a11y-click-events-have-key-events -->
						<img
							src={`${src}/${version}`}
							alt="Summary of the text next to it."
							class="m-1 block max-w-24 max-h-24 cursor-pointer"
							on:error={() => handleImageError()}
							on:click={() => setSelectedImage(version)}
						/>
					{/each}
				</div>
				<h3>Prompt:</h3>
				<textarea on:input={handleTextareaInput} rows="3" class="mt-2 w-full">{prompt}</textarea>
				<div class="flex">
					<div>
						{#if userModifiedPrompt}
							<button on:click={resetUserModifiedPrompt}> Reset prompt </button>
						{/if}
					</div>
					<div class="ml-auto">
						<button on:click={() => generateImage()}>
							{isGenerating ? 'Generating...' : 'Generate image'}
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
			{isGenerating ? 'Generating...' : 'Generate image'}
		</button>
		{#if errorMessage}
			<p class="text-red-600">{errorMessage}</p>
		{/if}
	{/if}
</div>
