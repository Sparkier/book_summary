<script lang="ts">
	import { fade } from 'svelte/transition';

	import ImageComponent from './ImageComponent.svelte';
	import TextComponent from './TextComponent.svelte';

	export let text: string;
	export let image: string;
</script>

<div transition:fade>
	<div class="flex-item">
		<div class="flex flex-row border-t-4">
			<TextComponent {text} />
			<ImageComponent src={image} {text} />
		</div>
	</div>
</div>
