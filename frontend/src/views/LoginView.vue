<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const router = useRouter();
const email = ref("admin@umkm.com");
const password = ref("Admin123!");
const error = ref("");

async function submit() {
  error.value = "";
  try {
    await auth.login(email.value, password.value);
    await router.push("/dashboard");
  } catch (err) {
    error.value = err instanceof Error ? err.message : "Login gagal";
  }
}
</script>

<template>
  <section class="auth-layout">
    <div class="auth-brand-panel">
      <div class="brand">
        UMKM
        <span class="brand-light">Pro</span>
      </div>
      <div class="auth-copy">
        <p class="eyebrow">OPERASIONAL LEBIH CERDAS</p>
        <h1>Semua angka.<br /><em>Satu arah.</em></h1>
        <p>Kelola keuangan dan operasional usaha lokal Anda dengan tenang.</p>
      </div>
      <span class="auth-decoration">✦</span>
    </div>
    <div class="auth-form-panel">
      <form class="auth-card" @submit.prevent="submit">
        <p class="eyebrow">SELAMAT DATANG KEMBALI</p>
        <h2>Masuk ke akun Anda</h2>
        <p class="muted">Lanjutkan mengelola pertumbuhan bisnis Anda.</p>
        <div v-if="error" class="alert alert-error">{{ error }}</div>
        <label
          >Email<input
            v-model="email"
            type="email"
            required
            autocomplete="email"
        /></label>
        <label
          >Password<input
            v-model="password"
            type="password"
            required
            autocomplete="current-password"
        /></label>
        <button
          class="button button-primary button-wide"
          :disabled="auth.loading"
          type="submit"
        >
          {{ auth.loading ? "Memproses..." : "Masuk" }}
        </button>
        <p class="auth-switch">
          Belum punya akun?
          <RouterLink to="/register">Daftar sekarang</RouterLink>
        </p>
      </form>
    </div>
  </section>
</template>
