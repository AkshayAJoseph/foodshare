<script>
  import { handleBackButton } from "../script";
  handleBackButton("/");
  const go = () => {
    goto(login, { replaceState: true });
  };
</script>

<h1>Welcome to Foodshare</h1>
<a href="login">
  <button>Login</button>
</a>
