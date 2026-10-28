<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const router = useRouter();
const name = ref("");
const email = ref("");
const password = ref("");
const error = ref("");

async function submit() {
  error.value = "";
  try {
    await auth.register(name.value, email.value, password.value);
    await router.push("/dashboard");
  } catch (err) {
    error.value = err instanceof Error ? err.message : "Registrasi gagal";
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
        <p class="eyebrow">MULAI HARI INI</p>
        <h1>Bangun usaha<br /><em>lebih terarah.</em></h1>
        <p>Data yang jelas membantu keputusan yang lebih baik.</p>
      </div>
      <span class="auth-decoration">✦</span>
    </div>
    <div class="auth-form-panel">
      <form class="auth-card" @submit.prevent="submit">
        <p class="eyebrow">BUAT AKUN BARU</p>
        <h2>Mulai perjalanan Anda</h2>
        <p class="muted">Daftar gratis untuk mulai mencatat operasional.</p>
        <div v-if="error" class="alert alert-error">{{ error }}</div>
        <label>Nama usaha<input v-model="name" required minlength="2" /></label>
        <label>Email<input v-model="email" type="email" required /></label>
        <label
          >Password<input
            v-model="password"
            type="password"
            required
            minlength="8"
        /></label>
        <button
          class="button button-primary button-wide"
          :disabled="auth.loading"
          type="submit"
        >
          {{ auth.loading ? "Memproses..." : "Buat akun" }}
        </button>
        <p class="auth-switch">
          Sudah punya akun? <RouterLink to="/login">Masuk</RouterLink>
        </p>
      </form>
    </div>
  </section>
</template>
