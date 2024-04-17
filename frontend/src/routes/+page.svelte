<script lang="ts">
	import '../app.css';
	import BookListComponent from '../components/BookListComponent.svelte';
	import Heading from '../elements/Heading.svelte';

	export let data;
</script>

<header>
	<nav class="bg-white shadow">
		<div class="container mx-auto px-6 py-3">
			<div class="md:flex md:items-center md:justify-between">
				<div class="flex justify-between items-center">
					<div class="text-xl font-semibold text-gray-700">
						<a
							href="http://localhost:5173/"
							class="text-gray-800 text-xl font-bold hover:text-gray-700 md:text-2xl">Logo</a
						>
					</div>

					<!-- Mobile menu button -->
					<div class="flex md:hidden">
						<button
							type="button"
							class="text-gray-500 hover:text-gray-600 focus:outline-none focus:text-gray-600"
							aria-label="toggle menu"
						>
							<svg viewBox="0 0 24 24" class="h-6 w-6 fill-current">
								<path
									fill-rule="evenodd"
									d="M4 5h16a1 1 0 0 1 0 2H4a1 1 0 1 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2z"
								/>
							</svg>
						</button>
					</div>
				</div>

				<!-- Mobile Menu open: "block", Menu closed: "hidden" -->
				<div class="hidden -mx-4 md:flex md:items-center">
					<a
						href="/#"
						class="block mx-4 mt-2 md:mt-0 text-sm text-gray-700 capitalize hover:text-blue-600"
						>About</a
					>
				</div>
			</div>
		</div>
	</nav>

	<div
		class="w-full bg-cover bg-center"
		style="height:32rem; background-image: url(BookShelf_Cover.jpg);"
	>
		<div class="flex items-center justify-center h-full">
			<div class="text-center">
				<h1 class="text-white text-2xl font-semibold md:text-3xl">Book Summarizer</h1>
				<p class="text-white md:text-2xl">Upload a book and auto-generate a summary and images</p>
			</div>
		</div>
	</div>
</header>

<div class="text-center pt-5">
	<Heading heading={'Library'} />
</div>

<BookListComponent books={data.books} />
