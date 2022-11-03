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
  image={`http://127.0.0.1:5000/api/get_paragraph_summary_image/${selectedBook}/${chapterIndex + 1}/${paragraphIndex}`}
/>
