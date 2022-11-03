<script lang="ts">
  import SummaryElement from "../SummaryElement.svelte";

  import { toSafeFilename } from "../../util";

  export let selectedBook: string;
  export let chapterIndex: number;
  export let paragraph: string;
  export let paragraphIndex: number;
</script>

<SummaryElement
  text={paragraph}
  image={`books/${selectedBook}/chapters/${
    chapterIndex + 1
  }/paragraphs/${paragraphIndex}-${toSafeFilename(`${paragraph}`)}.png`}
/>
