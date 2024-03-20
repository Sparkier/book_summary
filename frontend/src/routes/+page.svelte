<script lang="ts">
	import '../app.css';
	import BookListComponent from '../components/BookListComponent.svelte';
	import Heading from '../elements/Heading.svelte';

	export let data;

	function addBook() {
		// books.push({ title: `Book ${books.length + 1}`, author: `Author ${books.length + 1}` });
	}
</script>

<div>
	<Heading heading={'Library'} />
</div>

<BookListComponent books={data.books} />
