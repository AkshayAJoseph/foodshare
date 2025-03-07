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
                    <h1>Contribute a food item</h1>
                    <h5>AI Scan</h5>
                </div>
                <div class="form">
                    <div class="form__row">
                        <label>Title</label>
                        <input placeholder="Thrissur" required />
                    </div>
                    <div class="form__row">
                        <label>Category</label>
                        <div class="flex">
                            <div class="form__option">
                                <h5>Veg</h5>
                            </div>
                            <div class="form__option">
                                <h5>Non Veg</h5>
                            </div>
                        </div>
                    </div>
                    <div class="form__row">
                        <label>Lifespan</label>
                        <input placeholder="Thrissur" required />
                    </div>
                    <div class="form__row">
                        <label>Count</label>
                        <input placeholder="Thrissur" required />
                    </div>
                    <div class="form__row">
                        <label>Tags</label>
                        <input placeholder="Thrissur" required />
                    </div>
                    <a href="/home">
                        <div class="btn--black">Contribute</div>
                    </a>
                </div>
            </div>
        </div>
        <button onclick={logout}>logout</button>
        <br />
    {/if}
    <Navigation />
</main>
