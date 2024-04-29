<script lang="ts">
	import { twMerge } from 'tailwind-merge';

	export let disabled = false;
	export let classNames = '';
</script>

<button class={twMerge('rounded border border-grey p-2', classNames)} on:click {disabled}>
	<slot />
</button>
