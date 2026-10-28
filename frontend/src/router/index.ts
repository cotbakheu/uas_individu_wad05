import { createRouter, createWebHistory } from "vue-router";

import { useAuthStore } from "@/stores/auth";
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";
import CategoriesView from "@/views/CategoriesView.vue";
import ProductsView from "@/views/ProductsView.vue";
import TransactionsView from "@/views/TransactionsView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", redirect: "/dashboard" },
    { path: "/login", component: LoginView, meta: { guest: true } },
    { path: "/register", component: RegisterView, meta: { guest: true } },
    { path: "/categories", component: CategoriesView, meta: { auth: true } },
    { path: "/products", component: ProductsView, meta: { auth: true } },
    {
      path: "/transactions",
      component: TransactionsView,
      meta: { auth: true },
    },
  ],
});

router.beforeEach(async (to) => {
  const auth = useAuthStore();
  await auth.restore();
  if (to.meta.auth && !auth.isAuthenticated) return "/login";
  if (to.meta.guest && auth.isAuthenticated) return "/dashboard";
});

export default router;
