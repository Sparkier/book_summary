<script lang="ts">
	import { page } from '$app/stores';
</script>

{#if $page.error}
	<h1>{$page.error.message}</h1>
{:else}
	<div>
		<h1>Are you sure this is what you are looking for? I get a 404 here 🙈</h1>
	</div>
{/if}
