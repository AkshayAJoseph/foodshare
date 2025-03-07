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
    import Progress from "$lib/Progress.svelte";
</script>

<main>
    <Progress order="2" />
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
                    <div class="flex">
                        <a href="/signup">
                            <div class="btn--black btn--outline">Register</div>
                        </a>
                        <a {onclick}>
                            <div class="btn--black">Log In</div>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</main>

<style>
    .flex {
        justify-content: space-between;
    }
    .flex > a {
        flex: 1;
    }
</style>
