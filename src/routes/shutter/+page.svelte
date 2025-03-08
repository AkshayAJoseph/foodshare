<script>
    import { onMount } from "svelte";
    import { checkUser, logout } from "../../script";
    import { takephoto } from "../../script";
    let data;
    let loading = true;
    let selectedCategory = "";
    let title = "";
    let lifespan = "";
    let count = "";
    let tags = "";

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

    const submitData = () => {
        const formData = {
            title: title,
            category: selectedCategory,
            lifespan: lifespan,
            count: count,
            tags: tags,
        };
        console.log(formData);
        // Here you would typically send formData to your backend
        // For now, we'll just log it
    };
</script>

<main>
    {#if loading}
        <p>Loading...</p>
    {:else}
        <Header h1="Welcome," h5={data.name} />
        <div class="box">
            <div class="flex">
                <a onclick={capture} class="small card--green">
                    <img src="/aperture.svg" alt="" />
                    <h1>Scan Food with ease</h1>
                </a>
            </div>
            <div class="card">
                <div class="card__title">
                    <h1>AI Capture</h1>
                    <h5>Scan</h5>
                </div>
                <div class="form">
                    <div class="form__row">
                        <label>Title</label>
                        <input
                            placeholder="Laddu"
                            bind:value={title}
                            required
                        />
                    </div>
                    <div class="form__row">
                        <label>Category</label>
                        <div class="flex">
                            <div
                                class="form__option"
                                class:selected={selectedCategory === "Veg"}
                                onclick={() => (selectedCategory = "Veg")}
                            >
                                <h5>Veg</h5>
                            </div>
                            <div
                                class="form__option"
                                class:selected={selectedCategory === "Non Veg"}
                                onclick={() => (selectedCategory = "Non Veg")}
                            >
                                <h5>Non Veg</h5>
                            </div>
                        </div>
                    </div>
                    <div class="form__row">
                        <label>Lifespan</label>
                        <input
                            placeholder="60Hours"
                            bind:value={lifespan}
                            required
                        />
                    </div>
                    <div class="form__row">
                        <label>Count</label>
                        <input placeholder="3" bind:value={count} required />
                    </div>
                    <div class="form__row">
                        <label>Tags</label>
                        <input placeholder="FRESH" bind:value={tags} required />
                    </div>
                    <div onclick={submitData} class="btn--black">
                        Contribute
                    </div>
                </div>
            </div>
        </div>
        <br />
    {/if}
    <Navigation />
</main>

<style>
    .flex {
        width: 100%;
        justify-content: center;
    }
    a.small {
        gap: 1rem;
        background: var(--color-white);
    }
    .card--green h1 {
        font-size: 1rem;
        color: var(--color-text);
    }
    .form__option {
        padding: 8px 16px;
        border: 1px solid #ccc;
        cursor: pointer;
        margin: 4px;
    }
    .form__option.selected {
        background-color: #e0f7fa;
        border-color: #00bcd4;
    }
</style>
