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
</script>

<h1>Login</h1>
<label>email</label>
<input type="text" placeholder="hari@laddu.cc" bind:value={email} />
<label>password</label>
<input type="password" bind:value={password} />
<label>name</label>
<input bind:value={name} />
<button {onclick}>signup</button>
