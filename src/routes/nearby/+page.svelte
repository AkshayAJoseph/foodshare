<script>
    import { getCoords, getDistance, getfoods } from "../../script";
    import { onMount } from "svelte";

    let selectedValue = $state(0); // Default integer value

    let data = $state([]);
    let loading = $state(true);

    const doFetch = async () => {
        data = await getfoods();
        console.log("Before Sorting:", data);
        const ucoords = await getCoords();
        const lonu = ucoords.longitude;
        const latu = ucoords.latitude;
        console.log(ucoords);

        data = data.map((item) => ({
            ...item,
            distance: getDistance(latu, lonu, item.latitude, item.longitude),
        }));
        data.sort((a, b) => a.distance - b.distance);
        console.log("After Sorting:", data);
        loading = false;
    };

    onMount(() => {
        doFetch();
    });
</script>

<main>
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
                            <p>{item.distance}</p>
                        </div>
                        <div class="card__row__buttons">
                            <h5>{item.stats || item.quantity}</h5>
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
