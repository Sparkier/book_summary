<script lang="ts">
  import SummaryElement from "../SummaryElement.svelte";

  import type { Chapter } from "../../types";
  import { toSafeFilename } from "../../util";

  export let selectedBook: string;
  export let chapterIndex: number;
  export let chapter: Chapter;
</script>

<SummaryElement
  text={chapter.chapter_summary}
  image={`books/${selectedBook}/chapters/${
    chapterIndex + 1
  }/chapter_summary/0-${toSafeFilename(`${chapter.chapter_summary}`)}.png`}
/>
