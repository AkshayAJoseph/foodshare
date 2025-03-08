<script>
    import { onMount } from "svelte";

    let currentPath = location.pathname;

    function isActive(path) {
        return currentPath == path;
    }
</script>

<main>
    <div class="nav">
        <a href="/home" class="small" class:active={isActive("/home")}>
            <img src="/house-circle-check.svg" alt="" />
        </a>
        <a href="/stats" class="small" class:active={isActive("/stats")}>
            <img src="/plant-growth.svg" alt="" />
        </a>
        <a href="/settings" class="small" class:active={isActive("/settings")}>
            <img src="/settings.svg" alt="" />
        </a>
        <a class="small" class:active={isActive("/connect")}>
            <img src="/circle-nodes.svg" alt="" />
        </a>
    </div>
</main>

<style>
    .nav {
        display: flex;
        justify-content: center;
        align-items: center;
        position: fixed;
        width: 100%;
        bottom: 2rem;
        gap: 1rem;
    }
    a.small {
        background: var(--color-primary);
        padding: 1rem;
        border-radius: 100rem;
        display: flex;
    }
    a.small img {
        filter: invert(57%) sepia(83%) saturate(4879%) hue-rotate(56deg)
            brightness(95%) contrast(99%);
        width: 20px;
        height: 20px;
    }

    a.small.active {
        background: var(--color-primary-dark);
    }

    a.small.active img {
        filter: invert(89%) sepia(23%) saturate(443%) hue-rotate(55deg)
            brightness(105%) contrast(101%);
    }
</style>
