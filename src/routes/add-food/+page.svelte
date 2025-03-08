<script>
    import { Storage } from "@capacitor/storage";
    import { onMount } from "svelte";
    import { Geolocation } from "@capacitor/geolocation";
    import Header from "$lib/Header.svelte";
    import Navigation from "$lib/Navigation.svelte";
    import {
        addfood,
        getArr,
        handleBackButton,
        login,
        takephoto,
    } from "../../script";

    let items = [];

    async function fetchData() {
        items = await getArr();
    }

    const addSection = async () => {
        items = await takephoto();
        console.log(items);
    };

    const clear = async () => {
        await Storage.remove({ key: "foodItems" });
    };

    const handleSubmit = async (index) => {
        const data = await Geolocation.getCurrentPosition();
        const { latitude, longitude } = data.coords;
        console.log(data);
        console.log("Submitting:", JSON.stringify(items[index]));
        addfood(items[index], longitude, latitude);
        console.log(index);
        if (items.length == 1) {
            items = [];
            Storage.remove({ key: "foodItems" });
        }
        items.splice(index, 1);
        items = items;
        await Storage.set({
            key: "foodItems",
            value: JSON.stringify(items),
        });
    };

    onMount(() => {
        fetchData();
    });

    handleBackButton("/");
</script>

<main>
    <Header h1="Scan easily" h5="with AI" />
    <div class="box">
        <div class="flex">
            <a onclick={addSection} class="small card--green">
                <img src="/aperture.svg" alt="" />
                <h1>Scan Food with ease</h1>
            </a>
        </div>
        {#each items as item, index}
            <div class="card">
                <div class="card__title">
                    <h1>AI Capture</h1>
                    <h5 onclick={clear}>Scan</h5>
                </div>
                <div class="form">
                    <div class="form__row">
                        <label>Title</label>
                        <input
                            placeholder="Laddu"
                            bind:value={item.name}
                            required
                        />
                    </div>

                    <div class="form__row">
                        <label>Lifespan</label>
                        <input
                            placeholder="60Hours"
                            bind:value={item.lifespan}
                            required
                        />
                    </div>
                    <div class="form__row">
                        <label>Count</label>
                        <input
                            placeholder="3"
                            bind:value={item.quantity}
                            required
                        />
                    </div>
                    <div class="form__row">
                        <label>Tags</label>
                        <input
                            placeholder="FRESH"
                            bind:value={item.tags}
                            required
                        />
                    </div>
                    <!-- svelte-ignore a11y_no_static_element_interactions -->
                    <!-- svelte-ignore a11y_click_events_have_key_events -->
                    <div onclick={() => handleSubmit(index)} class="btn--black">
                        Contribute
                    </div>
                </div>
            </div>
        {/each}
    </div>
    <br />
    <Navigation />
</main>

<style>
    .flex {
        width: 100%;
        justify-content: center;
        margin-top: 2rem;
    }
    a.small {
        gap: 1rem;
        background: var(--color-white);
    }
    .card--green h1 {
        font-size: 1rem;
        color: var(--color-text);
    }
</style>
