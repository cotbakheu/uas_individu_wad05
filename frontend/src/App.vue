<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";

import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const route = useRoute();
const router = useRouter();

async function signOut() {
  await auth.logout();
  await router.push("/login");
}
</script>

<template>
  <div
    v-if="auth.initialized"
    class="app-shell"
    :class="{ 'public-shell': !auth.isAuthenticated }"
  >
    <header v-if="auth.isAuthenticated" class="topbar">
      <RouterLink class="brand" to="/dashboard">
        <span>UMKM <span class="brand-light">Pro</span></span>
      </RouterLink>
      <nav class="main-nav">
        <RouterLink to="/dashboard">Dashboard</RouterLink>
        <RouterLink to="/transactions">Transaksi</RouterLink>
        <RouterLink to="/products">Produk</RouterLink>
        <RouterLink to="/categories">Kategori</RouterLink>
      </nav>
      <div class="user-menu">
        <span class="user-avatar">{{
          auth.user?.name.slice(0, 1).toUpperCase()
        }}</span>
        <span class="user-name">{{ auth.user?.name }}</span>
        <button
          class="button button-ghost button-small"
          :disabled="auth.loading"
          @click="signOut"
        >
          {{ auth.loading ? "Keluar..." : "Keluar" }}
        </button>
      </div>
    </header>
    <main :class="{ 'page-container': auth.isAuthenticated }">
      <div v-if="auth.isAuthenticated" class="page-eyebrow">
        {{ route.name }}
      </div>
      <RouterView />
    </main>
  </div>
  <div v-else class="loading-screen">Memuat aplikasi...</div>
</template>
