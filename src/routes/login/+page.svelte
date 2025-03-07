<script>
    import { handleBackButton, login } from "../../script";
    let email = $state("");
    let password = $state("");
    handleBackButton("/");
    const onclick = () => {
        if (email != "" && password != "") {
            const data = { email, password };
            login(data);
        } else {
            alert("Please fill in every fields");
        }
    };
    import Header from "$lib/Header.svelte";
    import Navigation from "$lib/Navigation.svelte";
    import Progress from "$lib/Progress.svelte";
</script>

<main>
    <Progress order="1" />
    <Header h1="Log in" h5="Personal Details" />
    <div class="box">
        <div class="card">
            <div class="card__title">
                <h1>Please Fill</h1>
            </div>
            <div class="form">
                <div class="form__row">
                    <div class="form__row">
                        <label>Email</label>
                        <input
                            type="text"
                            placeholder="hari@laddu.cc"
                            bind:value={email}
                            required
                        />
                    </div>
                    <div class="form__row">
                        <label>Password</label>
                        <input
                            type="password"
                            bind:value={password}
                            placeholder="********"
                            required
                        />
                    </div>
                    <a href="/home" {onclick}>
                        <div class="btn--black">Register</div>
                    </a>
                </div>
            </div>
        </div>
    </div>
</main>

<style>
</style>
