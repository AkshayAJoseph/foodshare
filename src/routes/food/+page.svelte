<script>
    import RazerPay from "$lib/RazerPay.svelte";
    import Header from "$lib/Header.svelte";
    import Navigation from "$lib/Navigation.svelte";
</script>

<main>
    <Navigation />
    <Header h1="Complete the payment" h5="Secured with RazerPay" />
    <div class="box">
        <div class="card">
            <div class="card__title">
                <h1>Initialise payment</h1>
            </div>
            <br />
            <a href="/home">
                <RazerPay />
                <div class="btn--black">Home</div>
            </a>
        </div>
    </div>
</main>

<style>
    a {
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 2rem;
        align-items: center;
    }
</style>
