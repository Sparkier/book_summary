<script lang="ts">
	import BookCard from '../elements/BookCard.svelte';

	export let books: { uuid: string; title: string; creator: string }[];
</script>

<div class="flex flex-wrap justify-start gap-4">
	{#each books as book (book.uuid)}
		<a href="/book/{book.uuid}">
			<BookCard
				title={book.title}
				imageSrc={`/api/books/${book.uuid}/images/0`}
				creator={book.creator}
			/>
		</a>
	{/each}
</div>
