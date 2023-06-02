<script lang="ts">
	import SubHeading from '../elements/SubHeading.svelte';
	import SummaryElement from './SummaryElement.svelte';

	import type { Book } from '../types';
	import { AbstractionLevel } from '../types';

	export let book: Book;
	export let selectedBook: string;
	export let abstractionLevel: AbstractionLevel;
</script>

<div class="flex flex-col overflow-auto">
	{#if abstractionLevel === AbstractionLevel.BOOK}
		<SummaryElement
			text={book.book_summary}
			image={`/api/get_book_summary_image/${selectedBook}/0`}
		/>
	{:else}
		{#each book.chapters as chapter, chapterIndex}
			<SubHeading heading={chapter['title']} />
			{#if abstractionLevel === AbstractionLevel.CHAPTER}
				<SummaryElement
					text={chapter.chapter_summary}
					image={`/api/get_chapter_summary_image/${selectedBook}/${chapterIndex + 1}/0`}
				/>
			{:else if abstractionLevel === AbstractionLevel.PARAGRAPH}
				{#each chapter.paragraph_summaries as paragraphSummary, paragraphIndex}
					<SummaryElement
						text={paragraphSummary}
						image={`/api/get_paragraph_summary_image/${selectedBook}/${
							chapterIndex + 1
						}/${paragraphIndex}`}
					/>
				{/each}
			{:else}
				{#each chapter.paragraphs as paragraph, paragraphIndex}
					<SummaryElement
						text={paragraph}
						image={`/api/get_paragraph_image/${selectedBook}/${chapterIndex + 1}/${paragraphIndex}`}
					/>
				{/each}
			{/if}
		{/each}
	{/if}
</div>
