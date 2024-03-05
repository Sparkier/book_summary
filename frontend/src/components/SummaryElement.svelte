<script lang="ts">
	import { fade } from 'svelte/transition';

	import ImageComponent from './ImageComponent.svelte';
	import TextComponent from './TextComponent.svelte';

	export let text: string;
	export let image: string;
	export let style: string;
	export let characters: { name: string; description: string }[];
	export let readingMode: boolean;
</script>

<div transition:fade>
	<div class="flex-item">
		<div class="flex flex-row border-t-4">
			<TextComponent {text} {readingMode} />
			<ImageComponent src={image} {text} {style} {characters} {readingMode} />
		</div>
	</div>
</div>
