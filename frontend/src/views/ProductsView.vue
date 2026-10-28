<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { api } from '@/services/api'
import type { Category, Product } from '@/types'

const products = ref<Product[]>([])
const categories = ref<Category[]>([])
const error = ref('')
const loading = ref(false)
const filtering = ref(false)
const filters = ref({ search: '', category_id: '', min_stock: '', max_stock: '' })
const form = ref({ name: '', description: '', price: 0, stock: 0, category_id: 0 })
const money = (v: number) => new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(v)

async function load() {
  filtering.value = true
  try {
    products.value = await api.get<Product[]>('/products', filters.value)
    if (!form.value.category_id && categories.value[0]) form.value.category_id = categories.value[0].id
  } catch (e) { error.value = e instanceof Error ? e.message : 'Gagal memuat produk' }
  finally { filtering.value = false }
}
async function loadCategories() {
  try { categories.value = await api.get<Category[]>('/categories') }
  catch (e) { error.value = e instanceof Error ? e.message : 'Gagal memuat kategori' }
}
async function add() {
  loading.value = true
  try {
    await api.post('/products', form.value)
    form.value = { name: '', description: '', price: 0, stock: 0, category_id: categories.value[0]?.id ?? 0 }
    await load()
  } catch (e) { error.value = e instanceof Error ? e.message : 'Gagal menyimpan' }
  finally { loading.value = false }
}
async function remove(id: number) {
  if (!confirm('Hapus produk ini?')) return
  loading.value = true
  try { await api.delete(`/products/${id}`); await load() }
  catch (e) { error.value = e instanceof Error ? e.message : 'Gagal menghapus produk' }
  finally { loading.value = false }
}
function clearFilters() { filters.value = { search: '', category_id: '', min_stock: '', max_stock: '' } }
watch(filters, load, { deep: true })
onMounted(async () => { await loadCategories(); await load() })
</script>

<template>
  <div class="view-header"><div><p class="eyebrow">KATALOG</p><h1>Produk</h1><p class="muted">Kelola produk, harga, stok, dan deskripsi usaha Anda.</p></div></div>
  <div v-if="error" class="alert alert-error">{{ error }}</div>
  <section class="content-card compact"><div class="filter-grid"><input v-model="filters.search" placeholder="Cari nama produk..." /><select v-model="filters.category_id"><option value="">Semua kategori</option><option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option></select><input v-model="filters.min_stock" type="number" min="0" placeholder="Stok minimum" /><input v-model="filters.max_stock" type="number" min="0" placeholder="Stok maksimum" /><button class="button button-ghost" :disabled="filtering" @click="clearFilters">{{ filtering ? 'Memuat...' : 'Reset filter' }}</button></div></section>
  <section class="content-card"><div class="section-heading"><h2>Tambah produk</h2></div><form class="form-grid" @submit.prevent="add"><label>Nama produk<input v-model="form.name" required minlength="2" /></label><label>Harga<input v-model.number="form.price" type="number" min="0" required /></label><label>Stok awal<input v-model.number="form.stock" type="number" min="0" required /></label><label>Kategori<select v-model.number="form.category_id" required><option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option></select></label><label class="span-2">Deskripsi<input v-model="form.description" maxlength="500" placeholder="Deskripsi produk (opsional)" /></label><button class="button button-primary" :disabled="loading">{{ loading ? 'Menyimpan...' : 'Simpan produk' }}</button></form></section>
  <section class="content-card"><div class="section-heading"><h2>Daftar produk</h2><span class="count">{{ filtering ? 'Memuat...' : `${products.length} produk` }}</span></div><div v-if="filtering && !products.length" class="empty-state">Memuat produk...</div><div v-else-if="!products.length" class="empty-state">Tidak ada produk yang sesuai filter.</div><div v-for="item in products" :key="item.id" class="product-row"><div><strong>{{ item.name }}</strong><small>{{ item.category_name }} · Stok {{ item.stock }}</small><small>{{ item.description || 'Tidak ada deskripsi' }}</small></div><b>{{ money(item.price) }}</b><button class="button button-danger button-small" :disabled="loading" @click="remove(item.id)">Hapus</button></div></section>
</template>
