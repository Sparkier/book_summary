<script lang="ts">
	import type { SelectedImages } from '$lib/types';
	import { ViewMode } from '$lib/types';
	import { fade } from 'svelte/transition';
	import ImageComponent from './ImageComponent.svelte';
	import TextComponent from './TextComponent.svelte';

	export let text: string;
	export let image: string;
	export let style: string;
	export let characters: { name: string; description: string }[];
	export let readingMode: boolean;
	export let viewMode: ViewMode;
	export let selectedImages: SelectedImages;
	export let chapterIndex: number;
	export let paragraphIndex: number;
	export let selectedBook: string;
</script>

<div transition:fade>
	<div class="flex-item">
		<div class="flex flex-row">
			{#if readingMode}
				{#if viewMode == ViewMode.IMAGE}
					<div class="ml-4 flex flex-wrap items-center m-1">
						<ImageComponent
							src={image}
							{text}
							{style}
							{characters}
							{readingMode}
							{selectedImages}
							{chapterIndex}
							{paragraphIndex}
							{selectedBook}
						/>
					</div>
				{:else if viewMode == ViewMode.TEXT}
					<div class="w-full ml-4 flex items-center">
						<TextComponent {text} {readingMode} />
					</div>
				{:else if viewMode == ViewMode.IMAGE_AND_TEXT}
					<div class="w-full ml-4 flex items-center">
						<TextComponent {text} {readingMode} />
					</div>
					<div class="ml-4 flex items-center m-1">
						<ImageComponent
							src={image}
							{text}
							{style}
							{characters}
							{readingMode}
							{selectedImages}
							{chapterIndex}
							{paragraphIndex}
							{selectedBook}
						/>
					</div>
				{/if}
			{:else}
				<div class="w-full ml-4 flex items-center">
					<ImageComponent
						src={image}
						{text}
						{style}
						{characters}
						{readingMode}
						{selectedImages}
						{chapterIndex}
						{paragraphIndex}
						{selectedBook}
					/>
				</div>
			{/if}
		</div>
	</div>
</div>
