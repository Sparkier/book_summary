<script lang="ts">
	import BookCard from '../elements/BookCard.svelte';

	export let books: { uuid: string; title: string }[];
</script>

<div class="book-list">
	{#each books as book (book.uuid)}
		<a href="/book/{book.uuid}">
			<BookCard title={book.title} />
		</a>
	{/each}
</div>
