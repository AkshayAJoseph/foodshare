<script>
    import { handleBackButton, signup } from "../../script";
    let email = $state("");
    let password = $state("");
    let name = $state("");
    handleBackButton("/login");
    const onclick = () => {
        const data = { email, password, name };
        signup(data);
    };
    import Header from "$lib/Header.svelte";
    import Navigation from "$lib/Navigation.svelte";
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
                        <input bind:value={name} />
                    </div>
                    <div class="form__row">
                        <label>Email</label>
                        <input
                            type="text"
                            placeholder="hari@laddu.cc"
                            bind:value={email}
                        />
                    </div>
                    <div class="form__row">
                        <label>Password</label>
                        <input type="password" bind:value={password} />
                    </div>
                    <div class="btn--black">hey</div>
                </div>
            </div>
        </div>
    </div>
</main>

<style>
</style>
