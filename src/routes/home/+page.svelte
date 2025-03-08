<script>
    import { onMount } from "svelte";
    import { checkUser, logout, getfoods } from "../../script";
    import { takephoto } from "../../script";
    let data;
    let loading = true;
    let photoData = null;

    const capture = async () => {
        photoData = await takephoto();
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
    import { goto } from "$app/navigation";

    // Expiring Soon Logic
    let expiringFoods = [];
    let expiringLoading = true;
    let selectedExpiringFood = null; // Track selected expiring food
    let selectedFilter = "2 Hours"; // Default filter

    const fetchExpiringFoods = async () => {
        expiringFoods = await getfoods();
        expiringFoods.sort((a, b) => a.hours - b.hours);
        expiringLoading = false;
    };

    const filterFoods = () => {
        let hours = parseInt(selectedFilter.split(" ")[0]);
        if (isNaN(hours)) {
            return expiringFoods; // Return all if filter is invalid
        }
        return expiringFoods.filter((food) => food.lifespan <= hours);
    };

    const selectExpiring = (food) => {
        selectedExpiringFood = food;
    };

    const clearSelection = () => {
        selectedExpiringFood = null;
    };

    const setFilter = (filter) => {
        selectedFilter = filter;
    };

    onMount(() => {
        fetchExpiringFoods();
    });
</script>

<main>
    {#if loading || expiringLoading}
        <p>Loading...</p>
    {:else}
        <Header h1="Welcome," h5={data.name} />
        <div class="box">
            <div class="card card--green">
                <div class="card__title">
                    <h1>Contribute</h1>
                </div>
                <p>Offer surplus food to support community needs</p>
                <div class="card__small">
                    <a href="/add-food" class="small">
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
                    <h5
                        class:selected={selectedFilter === "2 Hours"}
                        onclick={() => setFilter("2 Hours")}
                    >
                        2 Hours
                    </h5>
                    <h5
                        class:selected={selectedFilter === "5 Hours"}
                        onclick={() => setFilter("5 Hours")}
                    >
                        5 Hours
                    </h5>
                    <h5
                        class:selected={selectedFilter === "10 Hours"}
                        onclick={() => setFilter("10 Hours")}
                    >
                        10 Hours
                    </h5>
                </div>
                {#if selectedExpiringFood}
                    <div class="card__row">
                        <div class="card__row__text">
                            <h1>{selectedExpiringFood.name}</h1>
                            <p>{selectedExpiringFood.lifespan} Hours</p>
                            <p>
                                <strong>Category:</strong>
                                {selectedExpiringFood.category}
                            </p>
                            <p>
                                <strong>Quantity:</strong>
                                {selectedExpiringFood.quantity}
                            </p>
                            <p>
                                <strong>Tags:</strong>
                                {selectedExpiringFood.tags}
                            </p>
                        </div>
                        <div class="card__row__buttons">
                            <button onclick={clearSelection}>Close</button>
                        </div>
                    </div>
                {:else}
                    {#each filterFoods().slice(0, 2) as food}
                        <!-- svelte-ignore a11y_click_events_have_key_events -->
                        <!-- svelte-ignore a11y_click_events_have_key_events -->
                        <!-- svelte-ignore a11y_no_static_element_interactions -->
                        <div
                            class="card__row"
                            onclick={() => selectExpiring(food)}
                        >
                            <div class="card__row__text">
                                <h1>{food.name}</h1>
                                <p>{food.lifespan} Hours</p>
                            </div>
                            <div class="card__row__buttons">
                                <h5>TAGS</h5>
                                <a href="/food">
                                    <img src="/eye.svg" alt="" />
                                </a>
                            </div>
                        </div>
                    {/each}
                {/if}
            </div>

            <div class="card">
                <div class="card__title">
                    <h1>Shortest Distance</h1>
                    <a href="/nearby">
                        <h5>See All</h5>
                    </a>
                </div>
                <p>check see all on a working phone</p>
            </div>
        </div>
        <br />
    {/if}
    <Navigation />
</main>

<style>
    .card--green p {
        width: 40%;
    }
    .selected {
        font-weight: bold;
    }
</style>
