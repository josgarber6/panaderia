<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import MyOrders from '@/components/Order/MyOrders.vue';

export default {
  components: {
    Navbar,
    Footer,
    MyOrders,
  },
};
</script>

<template>
  <Navbar />
  <MyOrders style="margin-bottom: 120px;"/>
  <Footer id="footer-bottom"/>

</template>