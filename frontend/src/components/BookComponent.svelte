<script lang="ts">
	import type { BookInfo } from '../types';

	export let book: BookInfo;

	function handleClick() {
		alert(`You clicked on ${book.title}`);
	}

	function handleAddClick() {
		alert('Add a new book');
	}
</script>

<div class="book-info">
	<h2>{book.title}</h2>
	<p>Author: {book.author}</p>
	<button on:click={handleClick}>Details</button>
</div>

<style>
	.book-info {
		border: 1px solid #ccc;
		padding: 20px;
		margin: 10px;
		width: 200px;
		height: 200px;
		display: inline-block;
		text-align: center;
	}
</style>
