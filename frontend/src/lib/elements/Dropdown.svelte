<script lang="ts">
	export let items: string[] | number[];
	export let value: string | number | undefined = undefined;
</script>

<select bind:value on:change class="rounded border border-grey mt-3">
	{#each items as item}
		<option value={item}>
			{item}
		</option>
	{/each}
</select>
