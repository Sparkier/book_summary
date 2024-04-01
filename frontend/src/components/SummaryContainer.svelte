<script lang="ts">
	import SubHeading from '../elements/SubHeading.svelte';
	import SummaryElement from './SummaryElement.svelte';

	import type { Book } from '../types';
	import { AbstractionLevel, ViewMode } from '../types';

	export let book: Book;
	export let selectedBook: string;
	export let abstractionLevel: AbstractionLevel;
	export let viewMode: ViewMode;
	export let style: string;
	export let characters: { name: string; description: string }[];
	export let readingMode: boolean;
</script>

<div class="flex flex-col overflow-auto">
	{#if abstractionLevel === AbstractionLevel.BOOK}
		<SummaryElement
			text={book.book_summary}
			image={`/api/books/${selectedBook}/images`}
			{style}
			{characters}
			{readingMode}
			{viewMode}
		/>
	{:else}
		{#each book.chapters as chapter, chapterIndex}
			<SubHeading heading={chapter['title']} />
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
						/>
					{/each}
				{/if}
			</div>
		{/each}
	{/if}
</div>
