<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import ListCategoriesAdmin from '@/components/Product/ListCategoriesAdmin.vue';

export default {
  name: 'AdminCategoriesView',
  components: {
    Navbar,
    Footer,
    ListCategoriesAdmin,
  },
};
</script>

<template>
  <div>
    <Navbar />
    <ListCategoriesAdmin />
    <Footer id="footer-bottom"/>
  </div>
</template>

<style>

</style>