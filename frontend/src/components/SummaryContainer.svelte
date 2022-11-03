<script lang="ts">
  import SubHeading from "../elements/SubHeading.svelte";
  import BookLevel from "./levels/BookLevel.svelte";
  import ChapterLevel from "./levels/ChapterLevel.svelte";
  import ParagraphLevel from "./levels/ParagraphLevel.svelte";
  import FullLevel from "./levels/FullLevel.svelte";

  import type { Book } from "../types";
  import { AbstractionLevel } from "../types";

  export let book: Book;
  export let selectedBook: string;
  export let abstractionLevel: AbstractionLevel;
</script>

<div class="flex flex-col overflow-auto">
  {#if abstractionLevel === AbstractionLevel.BOOK}
    <BookLevel {book} {selectedBook} />
  {:else}
    {#each book.chapters as chapter, chapterIndex}
      <SubHeading heading={chapter["title"]} />
      {#if abstractionLevel === AbstractionLevel.CHAPTER}
        <ChapterLevel {selectedBook} {chapterIndex} {chapter} />
      {:else if abstractionLevel === AbstractionLevel.PARAGRAPH}
        {#each chapter.paragraph_summaries as paragraphSummary, paragraphIndex}
          <ParagraphLevel
            {selectedBook}
            {chapterIndex}
            {paragraphSummary}
            {paragraphIndex}
          />
        {/each}
      {:else}
        {#each chapter.paragraphs as paragraph, paragraphIndex}
          <FullLevel
            {selectedBook}
            {chapterIndex}
            {paragraph}
            {paragraphIndex}
          />
        {/each}
      {/if}
    {/each}
  {/if}
</div>
