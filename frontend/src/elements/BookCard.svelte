<script lang="ts">
	export let title: string;
	export let creator: string;
	export let imageSrc: string;
</script>

<div class="border border-slate-200 w-64 h-full rounded-md">
	<img src={imageSrc} alt={'Book summary cover'} />
	<div class="p-2">
		<h3>{title}</h3>
		{#if creator}
			<p>{creator}</p>
		{/if}
	</div>
</div>
