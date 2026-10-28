<script setup lang="ts">
import { onMounted, ref } from "vue";
import { api } from "@/services/api";
import type { Category } from "@/types";

const items = ref<Category[]>([]);
const name = ref("");
const error = ref("");
const loading = ref(false);

async function load() {
  loading.value = true;
  try {
    items.value = await api.get<Category[]>("/categories");
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Gagal memuat kategori";
  } finally {
    loading.value = false;
  }
}
async function add() {
  if (!name.value.trim()) return;
  loading.value = true;
  try {
    await api.post("/categories", { name: name.value });
    name.value = "";
    await load();
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Gagal menyimpan";
  } finally {
    loading.value = false;
  }
}
async function remove(id: number) {
  if (confirm("Hapus kategori ini?")) {
    loading.value = true;
    try {
      await api.delete(`/categories/${id}`);
      await load();
    } catch (e) {
      error.value = e instanceof Error ? e.message : "Gagal menghapus kategori";
    } finally {
      loading.value = false;
    }
  }
}
onMounted(load);
</script>

<template>
  <div class="view-header">
    <div>
      <p class="eyebrow">KATALOG</p>
      <h1>Kategori</h1>
      <p class="muted">Kelompokkan produk agar lebih mudah dikelola.</p>
    </div>
  </div>
  <div v-if="error" class="alert alert-error">{{ error }}</div>
  <section class="content-card compact">
    <form class="inline-form" @submit.prevent="add">
      <input
        v-model="name"
        placeholder="Nama kategori baru"
        minlength="2"
        required
      /><button class="button button-primary" :disabled="loading">{{ loading ? "Menyimpan..." : "Tambah kategori" }}</button>
    </form>
  </section>
  <section class="content-card">
    <div class="section-heading">
      <h2>Semua kategori</h2>
      <span class="count">{{ items.length }} kategori</span>
    </div>
    <div v-if="loading && !items.length" class="empty-state">Memuat kategori...</div>
    <div v-else-if="!items.length" class="empty-state">Belum ada kategori.</div>
    <div v-for="item in items" :key="item.id" class="simple-row">
      <span>{{ item.name }}</span
      ><button
        class="button button-danger button-small"
        :disabled="loading"
        @click="remove(item.id)"
      >
        Hapus
      </button>
    </div>
  </section>
</template>
