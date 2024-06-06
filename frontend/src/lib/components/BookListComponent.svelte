<script lang="ts">
	import BookCard from '../elements/BookCard.svelte';
	import { fetchSelectedImages } from '$lib/api';

	export let books: { uuid: string; title: string; creator: string }[];
</script>

<div class="flex flex-wrap justify-start gap-4">
	{#each books as book (book.uuid)}
		{#await fetchSelectedImages(book.uuid)}
			Loading selection...
		{:then selectedImages}
			<a href="/book/{book.uuid}">
				<BookCard
					title={book.title}
					imageSrc={`/api/books/${book.uuid}/images/${selectedImages.bookSelectedId}`}
					creator={book.creator}
				/>
			</a>
		{:catch}
			<a href="/book/{book.uuid}">
				<BookCard
					title={book.title}
					imageSrc={`/api/books/${book.uuid}/images/0`}
					creator={book.creator}
				/>
			</a>
		{/await}
	{/each}
</div>
