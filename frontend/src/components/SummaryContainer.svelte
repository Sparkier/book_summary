<script lang="ts">
    import SummaryElement from "./SummaryElement.svelte";
    import { fade } from "svelte/transition";
    export let path: string;
    export let texts: string[];
    export let summaries: string[];
    function rstrip(x: string) {
        // This implementation removes whitespace from the right side
        // of the input string.
        return x.replace(/\s+$/gm, '');
    }

    function to_safe_filename(filename: string) {
        return rstrip(filename.substring(0, 250).replace(/[^a-z0-9 ]/gi, ''))
    }
  </script>
  <style>
.flex-container {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}
.flex-item {
  max-width:200px;
  margin: 0.25em;
}
  </style>
  <div class="flex-container">
{#each texts as text, i}
      <div transition:fade>
        <div class="flex-item">
            <SummaryElement text={text} summary={summaries[i]} image={path + i + "-" + to_safe_filename(summaries[i]) + '.png'} />
        </div>
    </div>
{/each}
</div>