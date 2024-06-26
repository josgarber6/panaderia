import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store.js'
import Cart from '@/components/Cart/Cart.vue'
import PaymentCompleted from '@/components/Payment/PaymentCompleted.vue'
import PaymentCancelled from '@/components/Payment/PaymentCancelled.vue'
import OrderCompleted from '@/components/Order/OrderCompleted.vue'
import MyOrders from '@/components/Order/MyOrders.vue'
import AdminEditProduct from '@/components/Product/AdminEditProduct.vue'
import AdminCreateProduct from '@/components/Product/AdminCreateProduct.vue'
import AdminEditCategory from '@/components/Product/AdminEditCategory.vue'
import AdminCreateCategory from '@/components/Product/AdminCreateCategory.vue'
import ListOrderAdmin from '@/components/Order/ListOrderAdmin.vue'
import AdminEditOrder from '@/components/Order/AdminEditOrder.vue'

import HomeView from '@/views/HomeView.vue'
import ProductsView from '@/views/ProductsView.vue'
import AdminProductsView from '@/views/AdminProductsView.vue'
import AdminCategoriesView from '@/views/AdminCategoriesView.vue'
import AdminStatsView from '@/views/AdminStatsView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/products',
      name: 'ProductsView',
      component: ProductsView
    },
    {
      path: '/cart',
      name: 'Cart',
      component: Cart
    },
    {
      path: '/payment/completed',
      name: 'PaymentCompleted',
      component: PaymentCompleted

    },
    {
      path: '/payment/cancelled',
      name: 'PaymentCancelled',
      component: PaymentCancelled
    },
    {
      path: '/order/completed',
      name: 'OrderCompleted',
      component: OrderCompleted
    },
    {
      path: '/order/my_orders',
      name: 'MyOrders',
      component: MyOrders
    },
    {
      path: '/admin/products',
      name: 'AdminProducts',
      component: AdminProductsView
    },
    {
      path: '/admin/products/new',
      name: 'AdminCreateProduct',
      component: AdminCreateProduct
    },
    {
      path: '/admin/products/:productId/edit',
      name: 'AdminEditProduct',
      component: AdminEditProduct
    },
    {
      path: '/admin/categories',
      name: 'AdminCategories',
      component: AdminCategoriesView
    },
    {
      path: '/admin/categories/new',
      name: 'AdminCreateCategory',
      component: AdminCreateCategory
    },
    {
      path: '/admin/categories/:categoryId/edit',
      name: 'AdminEditCategory',
      component: AdminEditCategory
    },
    {
      path: '/admin/orders',
      name: 'AdminOrders',
      component: ListOrderAdmin
    },
    {
      path: '/admin/orders/:orderId/edit',
      name: 'AdminEditOrder',
      component: AdminEditOrder
    },
    {
      path: '/admin/stats',
      name: 'AdminStatsView',
      component: AdminStatsView
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  await store.dispatch('getUserInfo');
  if (to.path.startsWith('/admin')) {
    if (!store.state.user) {
      next({name: 'home'});
    } else if(store.state.user.isAdmin) {
      next();
    } else {
      next({name: 'home'});
    }
  } else {
    next();
  }
});

export default router
