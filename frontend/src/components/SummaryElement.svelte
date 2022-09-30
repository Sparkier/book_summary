<script lang="ts">
  import ImageComponent from "./ImageComponent.svelte";
  import TextComponent from "./TextComponent.svelte";

  export let text: string;
</script>

<div class="flex flex-row border-t-4">
  <TextComponent {text} />
  <ImageComponent />
</div>
