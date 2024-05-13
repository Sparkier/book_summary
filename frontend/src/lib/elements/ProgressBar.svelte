<script lang="ts">
	import { twMerge } from 'tailwind-merge';
	export let progress: number;
	export let progressError: string | undefined = undefined;
	export let width: number = 200;

	export let classNames = '';
</script>

<div class={twMerge('w-full bg-gray-200 rounded-lg', classNames)} style="width:{width}px">
	<div
		class="bg-blue-500 text-xs leading-none py-1 text-center text-white rounded-lg"
		style="width: {Math.floor(progress)}%"
	>
		<p class="ml-1">{Math.floor(progress)}%</p>
		{#if progressError}
			<p class="text-red-600">{progressError}</p>
		{/if}
	</div>
</div>
