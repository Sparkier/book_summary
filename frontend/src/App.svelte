<script lang="ts">
  import ImageComponent from "./components/ImageComponent.svelte";
  import SummaryContainer from "./components/SummaryContainer.svelte";
  import TextComponent from "./components/TextComponent.svelte";
  import Heading from "./elements/Heading.svelte";
  import * as book from "./texts/alice_summarized.json";

  $: title = book.book["title"];
  $: chapters = book.book["chapters"];
  $: paragraphs = chapters[selectedChapter]["paragraphs"];
  $: paragraph_summaries = chapters[selectedChapter]["paragraph_summaries"];

  let selectedChapter = 0;

  function removeItem<T>(arr: Array<T>, value: T): Array<T> {
    const index = arr.indexOf(value);
    if (index > -1) {
      arr.splice(index, 1);
    }
    return arr;
  }
  function rstrip(x: string) {
        // This implementation removes whitespace from the right side
        // of the input string.
        return x.replace(/\s+$/gm, '');
    }

    function to_safe_filename(filename: string) {
        return rstrip(filename.substring(0, 250).replace(/[^a-z0-9 ]/gi, ''))
    }
</script>

<main>
  <div class="flex flex-col">
    <Heading heading={title} />
    <div class="p-2">
      <select bind:value={selectedChapter}>
        {#each chapters as chapter, i}
          <option value={i}>
            {chapter["title"]}
          </option>
        {/each}
      </select>
      <div class="flex flex-row">
        <ImageComponent src={'./books/' + to_safe_filename(title) + "/chapters/" + (selectedChapter+1) + "/chapter_summary/0-" + to_safe_filename(chapters[selectedChapter]["chapter_summary"]) + ".png"} />
        <TextComponent text={chapters[selectedChapter]["chapter_summary"]} />
      </div>
    </div>
    <Heading heading="Paragraphs" />
    <SummaryContainer path={'./books/' + to_safe_filename(title) + "/chapters/" + (selectedChapter+1) + '/paragraph_summaries/'} texts={paragraphs} summaries={paragraph_summaries}></SummaryContainer>
  </div>
</main>

<style global lang="postcss">
  @tailwind base;
  @tailwind elements;
  @tailwind utilities;
</style>
