<script lang="ts">
	import '../app.css';
	import AddBook from '../components/AddBook.svelte';
	import BookListComponent from '../components/BookListComponent.svelte';

	export let data;
</script>

<div
	class="w-full bg-cover bg-center"
	style="height:32rem; background-image: url(BookShelf_Cover.jpg);"
>
	<div class="flex items-center justify-center h-full">
		<div class="text-center">
			<h1 class="text-white">shelf</h1>
			<h4 class="text-white">Read and generate illustrated books in just the right length.</h4>
		</div>
	</div>
</div>

<div class="p-5 flex flex-col gap-3">
	<div class="flex gap-3 items-center">
		<h2>Library</h2>
		<AddBook />
	</div>
	<BookListComponent books={data.books} />
</div>
