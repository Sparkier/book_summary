<script lang="ts">
	export let title: string;
	export let creator: string;
	export let imageSrc: string;
	export let button: boolean = false;
	export let buttonMsg: string = '';
	export let btnDisabled: boolean = false;
</script>

<div class="flex flex-col border border-slate-200 w-64 h-full rounded-lg shadow-md">
	<img class="rounded-lg" src={imageSrc} alt={'Book summary cover'} />
	<div class="flex-1 flex flex-col justify-between p-2">
		<h3 class="text-xl font-bold text-center tracking-tight text-gray-900">
			{title}
		</h3>
		{#if creator}
			<p class="mb-4 text-sm font-medium text-center text-gray-600">{creator}</p>
		{/if}
		{#if button}
			<button
				class="bg-white hover:bg-gray-100 text-gray-800 font-semibold py-2 border border-gray-900 rounded-3xl shadow-self-center"
				disabled={btnDisabled}
			>
				{buttonMsg}
			</button>
		{/if}
	</div>
</div>
