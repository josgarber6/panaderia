<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import MyOrders from '@/components/Order/MyOrders.vue';

export default {
  data() {
    return {
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
  <template v-if="orders.length === 0">
    <Footer id="footer-bottom"/>
  </template>
  <template v-else>
    <Footer/>
  </template>
</template>