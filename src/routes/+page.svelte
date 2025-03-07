<script>
  import { goto } from "$app/navigation";
  import { checkUser, handleBackButton } from "../script";
  import { Storage } from "@capacitor/storage";
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

<h1>Welcome to Foodshare</h1>
<a href="login">
  <button>Login</button>
</a>
