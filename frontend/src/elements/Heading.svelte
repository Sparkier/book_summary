<script lang="ts">
	import { twMerge } from 'tailwind-merge';

	export let heading: string;
	export let classNames: string = '';
</script>

<h2 class={twMerge('text-2xl font-bold leading-7 pr-2 mt-2', classNames)}>
	{heading}
</h2>
