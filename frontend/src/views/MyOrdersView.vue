<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import MyOrders from '@/components/Order/MyOrders.vue';

export default {
  data() {
    return {
      // Declaramos orders para poder pasarla como prop a MyOrders
      orders: [],
    };
  },
  components: {
    Navbar,
    Footer,
    MyOrders,
  },
};
</script>

<template>
  <Navbar />
  <MyOrders :orders="orders"/>
  <!-- Gracias a orders en el return podemos ajustar el footer -->
  <template v-if="orders.length === 0">
    <Footer id="footer-bottom"/>
  </template>
  <template v-else>
    <Footer/>
  </template>
</template>