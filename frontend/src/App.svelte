<script lang="ts">
  import { fade } from "svelte/transition";
  import SummaryElement from "./components/SummaryElement.svelte";
  import Dropdown from "./elements/Dropdown.svelte";
  import Heading from "./elements/Heading.svelte";
  import * as book from "./texts/alice.json";

  $: keys = Object.keys(book.book);
  $: levels = removeItem([...keys], "title");
  $: texts = book.book[level];

  let level = "0";

  function removeItem<T>(arr: Array<T>, value: T): Array<T> {
    const index = arr.indexOf(value);
    if (index > -1) {
      arr.splice(index, 1);
    }
    return arr;
  }
</script>

<main>
  <div class="flex flex-col">
    <Heading heading={book.book["title"]} />
    <div class="p-2">
      <Dropdown items={levels} bind:value={level} />
    </div>
    {#each texts as text (text)}
      <div transition:fade>
        <SummaryElement {text} />
      </div>
    {/each}
  </div>
</main>

<style global lang="postcss">
  @tailwind base;
  @tailwind elements;
  @tailwind utilities;
</style>
