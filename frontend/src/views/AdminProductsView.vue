<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import ListProductAdmin from '@/components/Product/ListProductAdmin.vue';

export default {
  name: 'AdminProductsView',
  components: {
    Navbar,
    Footer,
    ListProductAdmin,
  },
};
</script>

<template>
  <div>
    <Navbar />
    <ListProductAdmin />
    <Footer/>
  </div>
</template>

<style>

</style>