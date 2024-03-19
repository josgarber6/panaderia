import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProductsView from '../views/ProductsView.vue'

import Cart from '../components/Cart/Cart.vue'
import PaymentCompleted from '../components/Payment/PaymentCompleted.vue'
import PaymentCancelled from '../components/Payment/PaymentCancelled.vue'
import OrderCompleted from '@/components/Order/OrderCompleted.vue'
import MyOrdersView from '@/views/MyOrdersView.vue'

const router = createRouter({
  // history: createWebHistory(import.meta.env.BASE_URL),
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
      component: MyOrdersView
    }
  ]
})

export default router
