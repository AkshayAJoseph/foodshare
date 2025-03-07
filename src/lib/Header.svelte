<script>
    export let h1;
    export let h5;
</script>

<main>
    <div class="box">
        <div class="box__text">
            <h1>{h1}</h1>
            <h5>{h5}</h5>
        </div>
        <div class="box__profile"></div>
    </div>
</main>

<style>
    .box {
        margin: 2rem auto;
    }
    h1 {
        margin-bottom: 0.5rem;
    }
    h5 {
        font-size: 1rem;
    }
</style>
