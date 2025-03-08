<script>
    import Header from "$lib/Header.svelte";
    import Navigation from "$lib/Navigation.svelte";
    import { getfoods } from "../../script";
    import { onMount } from "svelte";

    let data = [];
    let loading = true;

    const doFetch = async () => {
        data = await getfoods();
        data.sort((a, b) => a.hours - b.hours);

        loading = false;
    };

    onMount(() => {
        doFetch();
    });
</script>

<main>
    <Navigation />
    <Header h1="All Items" h5="Ordered by Expiry" />
    <div class="box">
        {#if loading}
            <p>loading</p>
        {:else}
            <div class="card">
                <div class="card__title">
                    <h1>Expiring Soon</h1>
                </div>

                {#each data as item}
                    <div class="card__row">
                        <div class="card__row__text">
                            <h1>{item.name}</h1>
                            <p>{item.lifespan} hours</p>
                        </div>
                        <div class="card__row__buttons">
                            <h5>{item.tags || item.quantity}</h5>
                            <a href="/food">
                                <img src="/eye.svg" alt="" />
                            </a>
                        </div>
                    </div>
                {/each}
            </div>
        {/if}
    </div>
</main>

<style>
    .form__option {
        cursor: pointer;
    }
    .form__option.selected {
        border: 2px solid green;
    }
</style>
