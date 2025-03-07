<script>
    export let h1;
    export let h5;
    import { checkUser, logout } from "../script";
</script>

<main>
    <div class="box">
        <div class="box__text">
            <h1>{h1}</h1>
            <h5>{h5}</h5>
        </div>
        <div class="box__profile">
            <a onclick={logout} class="small">
                <img src="/user.svg" alt="" />
            </a>
        </div>
    </div>
</main>

<style>
    .box {
        margin: 2rem auto;
        display: flex;
    }
    .box__text {
        flex: 1;
    }
    .box__profile {
        margin-right: 1rem;
    }
    h1 {
        margin-bottom: 0.5rem;
    }
    h5 {
        font-size: 1rem;
    }
</style>
