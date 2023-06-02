<script lang="ts">
	import '../app.css';
	import SummaryContainer from '../components/SummaryContainer.svelte';
	import Heading from '../elements/Heading.svelte';
	import { AbstractionLevel } from '../types';
	import { fetchBooks, fetchBook } from '../api';

	let selectedBook = 'Alices Adventures in Wonderland';

	let abstractionLevel = AbstractionLevel.BOOK;
</script>

<main class="overflow-hidden h-full">
	<div class="flex flex-col h-full">
		{#await fetchBooks() then books}
			<select bind:value={selectedBook}>
				{#each books as book}
					<option value={book}>
						{book}
					</option>
				{/each}
			</select>
			{#await fetchBook(selectedBook)}
				Loading book.
			{:then book}
				<Heading heading={book['title']} />
				<div class="py-2">
					<div class="flex">
						<p class="pr-2">Abstraction Level:</p>
						<select bind:value={abstractionLevel}>
							{#each Object.values(AbstractionLevel) as abstractionLevel}
								<option value={abstractionLevel}>
									{abstractionLevel}
								</option>
							{/each}
						</select>
					</div>
				</div>
				<SummaryContainer {book} {selectedBook} {abstractionLevel} />
			{:catch}
				Book could not be loaded.
			{/await}
		{/await}
	</div>
</main>
