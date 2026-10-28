<script setup lang="ts">
import { onMounted, ref } from "vue";
import { api } from "@/services/api";
import type { Summary, Transaction } from "@/types";

const summary = ref<Summary>({
  income: 0,
  expense: 0,
  balance: 0,
  transaction_count: 0,
  product_count: 0,
});
const recent = ref<Transaction[]>([]);
const error = ref("");
const loading = ref(true);
const money = (value: number) =>
  new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    maximumFractionDigits: 0,
  }).format(value);

onMounted(async () => {
  try {
    const [stats, transactions] = await Promise.all([
      api.get<Summary>("/dashboard/summary"),
      api.get<Transaction[]>("/transactions"),
    ]);
    summary.value = stats;
    recent.value = transactions.slice(0, 5);
  } catch (err) {
    error.value = err instanceof Error ? err.message : "Gagal memuat dashboard";
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="view-header">
    <div>
      <p class="eyebrow">RINGKASAN HARI INI</p>
      <h1>Dashboard</h1>
      <p class="muted">Pantau kesehatan usaha Anda dalam satu pandangan.</p>
    </div>
    <RouterLink class="button button-primary" to="/transactions"
      >+ Catat transaksi</RouterLink
    >
  </div>
  <div v-if="error" class="alert alert-error">{{ error }}</div>
  <div v-if="loading" class="loading-panel">Memuat dashboard...</div>
  <section v-else class="stats-grid">
    <article class="stat-card stat-highlight">
      <span class="stat-label">Saldo bersih</span
      ><strong>{{ money(summary.balance) }}</strong
      ><small>Posisi keuangan saat ini</small>
    </article>
    <article class="stat-card">
      <span class="stat-label">Total pemasukan</span
      ><strong>{{ money(summary.income) }}</strong
      ><small class="positive">↑ Pendapatan tercatat</small>
    </article>
    <article class="stat-card">
      <span class="stat-label">Total pengeluaran</span
      ><strong>{{ money(summary.expense) }}</strong
      ><small class="negative">↓ Biaya operasional</small>
    </article>
    <article class="stat-card">
      <span class="stat-label">Produk aktif</span
      ><strong>{{ summary.product_count }}</strong
      ><small>{{ summary.transaction_count }} transaksi tercatat</small>
    </article>
  </section>
  <section v-if="!loading" class="content-card">
    <div class="section-heading">
      <div>
        <p class="eyebrow">AKTIVITAS</p>
        <h2>Transaksi terbaru</h2>
      </div>
      <RouterLink to="/transactions">Lihat semua →</RouterLink>
    </div>
    <div v-if="!recent.length" class="empty-state">
      Belum ada transaksi. Mulai catat pemasukan atau pengeluaran Anda.
    </div>
    <div v-else class="transaction-list">
      <div v-for="item in recent" :key="item.id" class="transaction-row">
        <span class="transaction-icon" :class="item.type">{{
          item.type === "income" ? "↗" : "↘"
        }}</span>
        <div>
          <strong>{{ item.title }}</strong
          ><small>{{
            new Date(item.transaction_date).toLocaleDateString("id-ID")
          }}</small>
        </div>
        <b :class="item.type"
          >{{ item.type === "income" ? "+" : "-" }}{{ money(item.total_amount) }}</b
        >
      </div>
    </div>
  </section>
</template>
