<script lang="ts">
  import SummaryElement from "../SummaryElement.svelte";

  import { toSafeFilename } from "../../util";

  export let selectedBook: string;
  export let chapterIndex: number;
  export let paragraphSummary: string;
  export let paragraphIndex: number;
</script>

<SummaryElement
  text={paragraphSummary}
  image={`books/${selectedBook}/chapters/${
    chapterIndex + 1
  }/paragraph_summaries/${paragraphIndex}-${toSafeFilename(
    `${paragraphSummary}`
  )}.png`}
/>
