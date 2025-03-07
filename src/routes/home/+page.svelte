<script>
  import { onMount } from "svelte";
  import { checkUser, logout } from "../../script";
  import { takephoto } from "../../script";
  let data;
  let loading = true;

  const onclick = async () => {
    await takephoto();
  };
  const doCheck = async () => {
    data = await checkUser();
    if (data) {
      loading = false;
    }
  };
  const onclick2 = () => {
    logout();
  };

  onMount(() => {
    doCheck();
  });
</script>

{#if loading}
  <p>Loading...</p>
{:else}
  <h1>Hi {data.name}</h1>
  <br>
  <button onclick={onclick2}>logout</button>
  <br>
  <button {onclick}>add item</button>
{/if}
