<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { api } from "@/services/api";
import type { Product, Transaction } from "@/types";

const items = ref<Transaction[]>([]);
const products = ref<Product[]>([]);
const error = ref("");
const loading = ref(false);
const filtering = ref(false);
const filters = ref({
  search: "",
  type: "",
  product_id: "",
  date_from: "",
  date_to: "",
});
const form = ref({
  title: "",
  amount: 1,
  type: "income" as "income" | "expense",
  notes: "",
  transaction_date: new Date().toISOString().slice(0, 10),
  product_id: null as number | null,
});
const money = (value: number) =>
  new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    maximumFractionDigits: 0,
  }).format(value);
const selectedProduct = () =>
  products.value.find((product) => product.id === form.value.product_id);
const stockLimitExceeded = () => {
  const product = selectedProduct();
  return form.value.type === "income" && !!product && form.value.amount > product.stock;
};
async function load() {
  filtering.value = true;
  try {
    items.value = await api.get<Transaction[]>("/transactions", filters.value);
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Gagal memuat transaksi";
  } finally {
    filtering.value = false;
  }
}
async function loadProducts() {
  try {
    products.value = await api.get<Product[]>("/products");
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Gagal memuat produk";
  }
}
async function add() {
  error.value = "";
  if (stockLimitExceeded()) {
    error.value = `Stok tidak mencukupi. Stok tersedia: ${selectedProduct()?.stock ?? 0} unit.`;
    return;
  }
  loading.value = true;
  try {
    await api.post("/transactions", {
      ...form.value,
      transaction_date: new Date(form.value.transaction_date).toISOString(),
    });
    form.value = {
      title: "",
      amount: 1,
      type: "income",
      notes: "",
      transaction_date: new Date().toISOString().slice(0, 10),
      product_id: null,
    };
    await Promise.all([loadProducts(), load()]);
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Gagal menyimpan";
  } finally {
    loading.value = false;
  }
}
async function remove(id: number) {
  if (!confirm("Hapus transaksi ini?")) return;
  loading.value = true;
  try {
    await api.delete(`/transactions/${id}`);
    await Promise.all([loadProducts(), load()]);
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Gagal menghapus transaksi";
  } finally {
    loading.value = false;
  }
}
function clearFilters() {
  filters.value = {
    search: "",
    type: "",
    product_id: "",
    date_from: "",
    date_to: "",
  };
}
watch(filters, load, { deep: true });
onMounted(async () => {
  await loadProducts();
  await load();
});
</script>

<template>
  <div class="view-header">
    <div>
      <p class="eyebrow">KEUANGAN</p>
      <h1>Transaksi</h1>
      <p class="muted">
        Pilih produk terlebih dahulu, lalu catat jumlah unit yang masuk atau
        keluar.
      </p>
    </div>
  </div>
  <div v-if="error" class="alert alert-error">{{ error }}</div>
  <section class="content-card">
    <div class="section-heading"><h2>Catat transaksi</h2></div>
    <form class="form-grid" @submit.prevent="add">
      <label
        >Produk
        <select v-model="form.product_id" required :disabled="loading">
          <option :value="null" disabled>Pilih produk</option>
          <option
            v-for="product in products"
            :key="product.id"
            :value="product.id"
          >
            {{ product.name }} · stok {{ product.stock }}
          </option>
        </select></label
      ><label
        >Jenis<select v-model="form.type" :disabled="loading">
          <option value="income">Pemasukan (stok berkurang)</option>
          <option value="expense">Pengeluaran (stok bertambah)</option>
        </select></label
      ><label
        >Jumlah unit<input
          v-model.number="form.amount"
          type="number"
          min="1"
          :max="form.type === 'income' ? selectedProduct()?.stock : undefined"
          required
          :disabled="loading" /></label
      ><label
        >Tanggal<input
          v-model="form.transaction_date"
          type="date"
          required
          :disabled="loading" /></label
      ><label
        >Judul transaksi<input
          v-model="form.title"
          required
          minlength="2"
          :disabled="loading" /></label
      ><label
        >Catatan (opsional)<input
          v-model="form.notes"
          maxlength="500"
          :disabled="loading"
      /></label>
      <div v-if="selectedProduct()" class="form-hint span-2">
        Stok setelah transaksi:
        {{
          selectedProduct()!.stock +
          (form.type === "income" ? -form.amount : form.amount)
        }}
        unit
      </div>
      <div v-if="stockLimitExceeded()" class="form-hint form-hint-error span-2">
        Jumlah pemasukan tidak boleh melebihi stok tersedia
        ({{ selectedProduct()?.stock }} unit).
      </div>
      <button class="button button-primary" :disabled="loading || stockLimitExceeded()">
        {{ loading ? "Menyimpan..." : "Simpan transaksi" }}
      </button>
    </form>
  </section>
  <section class="content-card compact">
    <div class="filter-grid">
      <input
        v-model="filters.search"
        placeholder="Cari judul transaksi..."
      /><select v-model="filters.type">
        <option value="">Semua jenis</option>
        <option value="income">Pemasukan</option>
        <option value="expense">Pengeluaran</option></select
      ><select v-model="filters.product_id">
        <option value="">Semua produk</option>
        <option
          v-for="product in products"
          :key="product.id"
          :value="product.id"
        >
          {{ product.name }}
        </option></select
      ><input v-model="filters.date_from" type="date" /><input
        v-model="filters.date_to"
        type="date"
      /><button
        class="button button-ghost"
        :disabled="filtering"
        @click="clearFilters"
      >
        {{ filtering ? "Memuat..." : "Reset filter" }}
      </button>
    </div>
  </section>
  <section class="content-card">
    <div class="section-heading">
      <h2>Riwayat transaksi</h2>
      <span class="count">{{
        filtering ? "Memuat..." : `${items.length} transaksi`
      }}</span>
    </div>
    <div v-if="filtering && !items.length" class="empty-state">
      Memuat transaksi...
    </div>
    <div v-else-if="!items.length" class="empty-state">
      Tidak ada transaksi yang sesuai filter.
    </div>
    <div v-for="item in items" :key="item.id" class="transaction-row">
      <span class="transaction-icon" :class="item.type">{{
        item.type === "income" ? "↗" : "↘"
      }}</span>
      <div>
        <strong>{{ item.title }}</strong
        ><small
          >{{ item.amount }} unit ·
          {{ new Date(item.transaction_date).toLocaleDateString("id-ID") }} ·
          {{ item.notes || "Tanpa catatan" }}</small
        >
      </div>
      <b :class="item.type"
        >{{ item.type === "income" ? "+" : "-" }}{{ money(item.total_amount) }}</b
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
