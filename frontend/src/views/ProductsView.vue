<script>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import ListProduct from '@/components/Product/ListProduct.vue'

export default {
  name: 'ProductsView',
  components: {
    Navbar,
    Footer,
    ListProduct
  },
}

</script>

<template>
  <Navbar/>
  <ListProduct/>
  <Footer/>
</template>