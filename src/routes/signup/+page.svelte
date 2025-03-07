<script>
    import { handleBackButton, signup } from "../../script";
    let email = $state("");
    let password = $state("");
    let name = $state("");
    handleBackButton("/login");
    const onclick = () => {
        if (email != "" && password != "" && name != "") {
            const data = { email, password, name };
            signup(data);
        } else {
            alert("Please fill in every fields");
        }
    };
    import Header from "$lib/Header.svelte";
    import Progress from "$lib/Progress.svelte";
</script>

<main>
    <Progress order="1" />
    <Header h1="Sign up" h5="Personal Details" />
    <div class="box">
        <div class="card">
            <div class="card__title">
                <h1>Please Fill</h1>
            </div>
            <div class="form">
                <div class="form__row">
                    <div class="form__row">
                        <label>Are you an</label>
                        <div class="flex">
                            <div class="form__option">
                                <h5>Individual</h5>
                            </div>
                            <div class="form__option">
                                <h5>Organization</h5>
                            </div>
                        </div>
                    </div>
                    <div class="form__row">
                        <label>Name</label>
                        <input
                            bind:value={name}
                            placeholder="Hari Narayan"
                            required
                        />
                    </div>
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
