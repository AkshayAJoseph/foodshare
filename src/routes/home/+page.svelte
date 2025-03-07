<script>
  import { onMount } from "svelte";
  import { checkUser, logout } from "../../script";
  let data;
  let loading = true;
  const doCheck = async () => {
    data = await checkUser();
    if (data) {
      loading = false;
    }
  };
  const onclick = () => {
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
  <button {onclick}>logout</button>
{/if}
