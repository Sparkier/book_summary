<script lang="ts">
	import BookCard from '../elements/BookCard.svelte';

	export let books: { uuid: string; title: string; creator: string }[];
</script>

<div class="mx-auto">
	<div class="flex flex-wrap justify-start gap-4 m-3">
		<a href="http://localhost:5173/#">
			<BookCard title="Add book" imageSrc="EmptyImage.jpg" creator="" />
		</a>
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
</div>
