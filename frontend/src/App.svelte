<script lang="ts">
  import SummaryContainer from "./components/SummaryContainer.svelte";
  import Heading from "./elements/Heading.svelte";
  import { AbstractionLevel } from "./types";

  let selectedBook = "alice";
  $: fetchJson = fetch(`books/${selectedBook}/summarized.json`).then((res) =>
    res.json()
  );

  let abstractionLevel = AbstractionLevel.BOOK;
</script>

<main class="overflow-hidden h-full">
  <div class="flex flex-col h-full">
    {#await fetchJson}
      Loading book.
    {:then book}
      <Heading heading={book["title"]} />
      <div class="py-2">
        <div class="flex">
          <p class="pr-2">Abstraction Level:</p>
          <select bind:value={abstractionLevel}>
            {#each Object.values(AbstractionLevel) as abstractionLevel}
              <option value={abstractionLevel}>
                {abstractionLevel}
              </option>
            {/each}
          </select>
        </div>
      </div>
      <SummaryContainer {book} {selectedBook} {abstractionLevel} />
    {:catch}
      Book could not be loaded.
    {/await}
  </div>
</main>

<style global lang="postcss">
  @tailwind base;
  @tailwind elements;
  @tailwind utilities;
</style>
