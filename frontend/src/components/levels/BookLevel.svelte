<script lang="ts">
  import SummaryElement from "../SummaryElement.svelte";

  import type { Book } from "../../types";
  import { toSafeFilename } from "../../util";

  export let book: Book;
  export let selectedBook: string;
</script>

<SummaryElement
  text={book.book_summary}
  image={`http://127.0.0.1:5000/api/get_book_summary_image/${selectedBook}`}
/>
