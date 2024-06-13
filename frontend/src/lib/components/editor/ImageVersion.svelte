<script lang="ts">
	import Fa from 'svelte-fa';
	import { faCircleXmark } from '@fortawesome/free-solid-svg-icons';
	import { PUBLIC_BACKEND_URL } from '$env/static/public';
	import type { SelectedImages } from '$lib/types';
	import Button from '$lib/elements/Button.svelte';
	const API = PUBLIC_BACKEND_URL;

	export let src: string;
	export let version: integer;
	export let selectedVersion: integer;

	let errorMessage = '';

	function handleImageError() {
		errorMessage = 'No Image available';
	}

	function removeImage() {
		alert('Remove image version');
	}
</script>

<div id="container">
	<label on:click on:keypress>
		<input type="radio" value={version} bind:group={selectedVersion} />
		<img
			src={`${src}`}
			alt="Summary of the text next to it."
			class="m-1 block max-w-20 max-h-20 cursor-pointer"
			on:error={() => handleImageError()}
		/>
	</label>
	{#if version != selectedVersion}
		<button id="x" on:click={removeImage}>
			<Fa icon={faCircleXmark} color="red" class="bg-white" style="border-radius:50%"
		/>
		</button>
	{/if}
</div>

<style>
	/* HIDE RADIO */
	[type='radio'] {
		position: absolute;
		opacity: 0;
		width: 0;
		height: 0;
	}

	/* IMAGE STYLES */
	[type='radio'] + img {
		cursor: pointer;
	}

	/* CHECKED STYLES */
	[type='radio']:checked + img {
		outline: 2px solid rgb(100, 100, 100);
	}
	/* Remove button */
	#container {
		position: relative;
		margin-top: 0.5em;
	}

	#x {
		position: absolute;
		width: 1.25em;
		height: 1.25em;
		top: -0.25em;
		right: -0.25em;
		background-color:transparent;
	}
</style>
