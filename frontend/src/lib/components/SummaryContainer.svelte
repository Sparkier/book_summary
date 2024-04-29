<script lang="ts">
	import { fetchSelectedImages } from '$lib/api';
	import type { Book } from '$lib/types';
	import { AbstractionLevel, ViewMode } from '$lib/types';
	import SummaryElement from './SummaryElement.svelte';

	export let book: Book;
	export let selectedBook: string;
	export let abstractionLevel: AbstractionLevel;
	export let viewMode: ViewMode;
	export let style: string;
	export let characters: { name: string; description: string }[];
	export let readingMode: boolean;
</script>

<div class="flex flex-col overflow-auto h-">
	{#await fetchSelectedImages(selectedBook)}
		Loading selection...
	{:then selectedImages}
		{#if abstractionLevel === AbstractionLevel.BOOK}
			<SummaryElement
				text={book.book_summary}
				image={`/api/books/${selectedBook}/images`}
				{style}
				{characters}
				{readingMode}
				{viewMode}
				{selectedImages}
				chapterIndex={-1}
				paragraphIndex={-1}
				{selectedBook}
			/>
		{:else}
			{#each book.chapters as chapter, chapterIndex}
				<h3>{chapter['title']}</h3>
				<div
					class="flex {viewMode == ViewMode.IMAGE && readingMode
						? 'flex-wrap'
						: 'flex-col'} overflow-auto"
				>
					{#if abstractionLevel === AbstractionLevel.CHAPTER}
						<SummaryElement
							text={chapter.chapter_summary}
							image={`/api/books/${selectedBook}/chapters/${chapterIndex + 1}/images`}
							{style}
							{characters}
							{readingMode}
							{viewMode}
							{selectedImages}
							{chapterIndex}
							paragraphIndex={-1}
							{selectedBook}
						/>
					{:else if abstractionLevel === AbstractionLevel.PARAGRAPH}
						{#each chapter.paragraph_summaries as paragraphSummary, paragraphIndex}
							<SummaryElement
								text={paragraphSummary}
								image={`/api/books/${selectedBook}/chapters/${
									chapterIndex + 1
								}/summarized_paragraphs/${paragraphIndex}/images`}
								{style}
								{characters}
								{readingMode}
								{viewMode}
								{selectedImages}
								{chapterIndex}
								{paragraphIndex}
								{selectedBook}
							/>
						{/each}
					{:else}
						{#each chapter.paragraphs as paragraph, paragraphIndex}
							<SummaryElement
								text={paragraph}
								image={`/api/books/${selectedBook}/chapters/${
									chapterIndex + 1
								}/paragraphs/${paragraphIndex}/images`}
								{style}
								{characters}
								{readingMode}
								{viewMode}
								{selectedImages}
								{chapterIndex}
								{paragraphIndex}
								{selectedBook}
							/>
						{/each}
					{/if}
				</div>
			{/each}
		{/if}
	{:catch}
		<p class="text-red-600">{'SelectedImages could not be loaded.'}</p>
	{/await}
</div>
