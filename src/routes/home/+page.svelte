<script>
  import { logout } from "../../script";

  const onclick = () => {
    logout();
  };
</script>

<button {onclick}>logout</button>
