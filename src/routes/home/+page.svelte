<script>
    import { onMount } from "svelte";
    import { checkUser, logout } from "../../script";
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
</script>

<main>
    {#if loading}
        <p>Loading...</p>
    {:else}
        <Header h1="Welcome," h5={data.name} />
        <div class="box">
            <div class="card">
                <div class="card__title">
                    <h1>Nearby Contributions</h1>
                    <h5>See All</h5>
                </div>
                <div class="card__filters">
                    <h5 class="selected">VEG</h5>
                    <h5>Under 0KM</h5>
                    <h5>Under 5KM</h5>
                </div>
                <div class="card__row">
                    <div class="card__row__text">
                        <h1>Sambar, Rice</h1>
                        <p>200m</p>
                    </div>
                    <div class="card__row__buttons">
                        <h5>TAGS</h5>
                        <a href="/food">
                            <img src="/eye.svg" alt="" />
                        </a>
                    </div>
                </div>
            </div>
            <div class="card">
                <div class="card__title">
                    <h1>Expiring Soon</h1>
                    <h5>See All</h5>
                </div>
                <div class="card__filters">
                    <h5 class="selected">2 Hours</h5>
                    <h5>5 Hours</h5>
                    <h5>10 Hours</h5>
                </div>
                <div class="card__row">
                    <div class="card__row__text">
                        <h1>Appam, Curry</h1>
                        <p>500m</p>
                    </div>
                    <div class="card__row__buttons">
                        <h5>TAGS</h5>
                        <a href="/food">
                            <img src="/eye.svg" alt="" />
                        </a>
                    </div>
                </div>
                <div class="card__row">
                    <div class="card__row__text">
                        <h1>Soup</h1>
                        <p>200m</p>
                    </div>
                    <div class="card__row__buttons">
                        <h5>TAGS</h5>
                        <a href="/food">
                            <img src="/eye.svg" alt="" />
                        </a>
                    </div>
                </div>
            </div>
        </div>
        <button onclick={logout}>logout</button>
        <br />
        <button {capture}>add item</button>
    {/if}
    <Navigation />
</main>
