<script>
    import { onMount } from "svelte";

    export let order;
    onMount(() => {
        document.querySelectorAll(".bar")[order].style = "background: white";
    });
</script>

<main>
    <div class="bars">
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
    </div>
</main>

<style>
    .bars {
        display: flex;
        padding-top: 0.5vh;
        gap: 1vw;
    }
    .bar {
        content: "";
        flex: 1;
        background: var(--color-white-light);
        border-radius: 0.5rem;
        height: 0.5vh;
    }
</style>
