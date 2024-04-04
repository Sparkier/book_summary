<script lang="ts">
	import '../app.css';
	import BookListComponent from '../components/BookListComponent.svelte';
	import Heading from '../elements/Heading.svelte';

	export let data;
</script>

<div>
	<Heading heading={'Library'} />
</div>

<BookListComponent books={data.books} />
