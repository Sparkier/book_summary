<script lang="ts">
  import ImageComponent from "./ImageComponent.svelte";

  export let text: string;
  export let summary: string;
  export let image: string;

	function handleClick() {
		this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
	}
</script>
<style>

  /* Style the button that is used to open and close the collapsible content */
  .collapsible {
    background-color: #eee;
    color: #444;
    cursor: pointer;
    padding: 18px;
    width: 100%;
    border: none;
    text-align: left;
    outline: none;
    font-size: 15px;
  }
  

  
  /* Style the collapsible content. Note: hidden by default */
  .content {
    padding: 0 18px;
    display: none;
    overflow: hidden;
    background-color: #f1f1f1;
  }


</style>

<div>

<ImageComponent src={image}/>
  <button type="button" class="collapsible" on:click={handleClick}>{summary}</button>
  <div class="content">
    <p>{text}</p>
  </div>
  <style>
		/* this style tag will be inserted as-is */

    .collapsible:after {
      content: '\02795'; /* Unicode character for "plus" sign (+) */
      font-size: 13px;
      color: white;
      float: right;
      margin-left: 5px;
    }
  
    /* Add a background color to the button if it is clicked on (add the .active class with JS), and when you move the mouse over it (hover) */
    .active, .collapsible:hover {
      background-color: #ccc;
    }
    .active:after {
	  content: "\2796"; /* Unicode character for "minus" sign (-) */
  }
	</style>
</div>