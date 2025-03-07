<script>
    import { goto } from "$app/navigation";
    import { checkUser, handleBackButton } from "../script";
    import { Storage } from "@capacitor/storage";

    import Header from "$lib/Header.svelte";
    import Progress from "$lib/Progress.svelte";

    handleBackButton("/");
    const doCheck = async () => {
        const { value } = await Storage.get({ key: "token" });
        console.log(value);
        if (value) {
            goto("home", { replaceState: true });
            return;
        }
    };
    doCheck();
</script>

<main>
    <Progress order="0" />
    <Header h1="Welcome!" h5="Let's share food :)" />
    <div class="box">
        <div class="box__banner">
            <img src="/eating.svg" alt="" />
        </div>
        <div class="box__content">
            <h1><span>Foodshare</span> is always nearby</h1>
            <p>
                Become a part of a community that cares. Share your surplus
                food, connect with neighbors, and make a difference in the fight
                against food insecurity
            </p>
        </div>
    </div>
    <a href="/add-food">
        <div class="btn--black btn--fixed">Get Started</div>
    </a>
</main>

<style>
    main {
        background: var(--color-primary);
        min-height: 100vh;
    }
    .box__banner img {
        margin-top: 10vh;
        width: 100%;
    }
    .box__content {
        margin: 2rem auto;
    }
    .box__content h1 {
        font-size: 1.5rem;
    }
    .box__content h1 span {
        background: var(--color-text);
        color: var(--color-brand);
        padding: 0 0.25rem;
        transform: rotate(-1deg);
    }
    .box__content p {
        margin-top: 1rem;
    }
</style>
