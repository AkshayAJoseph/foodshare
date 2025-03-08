<script>
    import { onMount } from "svelte";
    import {
        checkUser,
        logout,
        getfoods,
        getCoords,
        getDistance,
    } from "../../script";
    import { takephoto } from "../../script";
    let data;
    let loading = true;

    const capture = async () => {
        await takephoto();
    };

    const doCheck = async () => {
        data = await checkUser();
        if (data) {
            loading = false;
        }
    };

    onMount(() => {
        doCheck();
    });
    import Header from "$lib/Header.svelte";
    import Navigation from "$lib/Navigation.svelte";

    // Expiring Soon Logic
    let expiringFoods = [];
    let expiringLoading = true;

    const fetchExpiringFoods = async () => {
        expiringFoods = await getfoods();
        expiringFoods.sort((a, b) => a.hours - b.hours);
        expiringLoading = false;
    };

    onMount(() => {
        fetchExpiringFoods();
    });

    // Nearby Contributions Logic
    let nearbyFoods = [];
    let nearbyLoading = true;

    const fetchNearbyFoods = async () => {
        let foods = await getfoods();
        const ucoords = await getCoords();
        const lonu = ucoords.longitude;
        const latu = ucoords.latitude;

        nearbyFoods = foods.map((item) => ({
            ...item,
            distance: getDistance(latu, lonu, item.latitude, item.longitude),
        }));
        nearbyFoods.sort((a, b) => a.distance - b.distance);
        nearbyLoading = false;
    };

    onMount(() => {
        fetchNearbyFoods();
    });
</script>

<main>
    {#if loading || expiringLoading || nearbyLoading}
        <p>Loading...</p>
    {:else}
        <Header h1="Welcome," h5={data.name} />
        <div class="box">
            <div class="card">
                <div class="card__title">
                    <h1>Nearby Contributions</h1>
                    <a href="/nearby">
                        <h5>See All</h5>
                    </a>
                </div>
                <div class="card__filters">
                    <h5 class="selected">Veg</h5>
                    <h5>10KM</h5>
                    <h5>5KM</h5>
                </div>
                {#each nearbyFoods.slice(0, 2) as food}
                    <div class="card__row">
                        <div class="card__row__text">
                            <h1>{food.name}</h1>
                            <p>{(food.distance * 1000).toFixed(0)}m</p>
                        </div>
                        <div class="card__row__buttons">
                            <h5>TAGS</h5>
                            <a href="/food">
                                <img src="/eye.svg" alt="" />
                            </a>
                        </div>
                    </div>
                {/each}
            </div>

            <div class="card card--green">
                <div class="card__title">
                    <h1>Contribute</h1>
                </div>
                <p>Offer surplus food to support community needs</p>
                <div class="card__small">
                    <a onclick={capture} class="small">
                        <img src="/aperture.svg" alt="" />
                    </a>
                    <a href="/upload" class="small">
                        <img src="/arrow-small-up.svg" alt="" />
                    </a>
                </div>
            </div>
            <div class="card">
                <div class="card__title">
                    <h1>Expiring Soon</h1>
                    <a href="/expiring">
                        <h5>See All</h5>
                    </a>
                </div>
                <div class="card__filters">
                    <h5 class="selected">2 Hours</h5>
                    <h5>5 Hours</h5>
                    <h5>10 Hours</h5>
                </div>
                {#each expiringFoods.slice(0, 2) as food}
                    <div class="card__row">
                        <div class="card__row__text">
                            <h1>{food.name}</h1>
                            <p>{(food.distance * 1000).toFixed(0)}m</p>
                        </div>
                        <div class="card__row__buttons">
                            <h5>TAGS</h5>
                            <a href="/food">
                                <img src="/eye.svg" alt="" />
                            </a>
                        </div>
                    </div>
                {/each}
            </div>
        </div>
        <button onclick={logout}>logout</button>
        <br />
    {/if}
    <Navigation />
</main>

<style>
    .card--green p {
        width: 40%;
    }
</style>
