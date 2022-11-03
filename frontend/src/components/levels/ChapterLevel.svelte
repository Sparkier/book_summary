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
  image={`http://127.0.0.1:5000/api/get_chapter_summary_image/${selectedBook}/${chapterIndex + 1}/0`}
/>
