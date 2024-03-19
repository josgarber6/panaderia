<script>
import { RouterLink } from 'vue-router';
import Navbar from '../Navbar.vue';
import Footer from '../Footer.vue';

export default {
  components: {
    Navbar,
    Footer,
    RouterLink,
  }
}

</script>

<template>
  <Navbar />
  <div class="container mt-4">
    <div class="card2 text-center">
      <div class="card-body">
        <h1 class="card-title">¡Pago cancelado!</h1>
        <p class="card-text">Tu pago ha sido cancelado.</p>
        <RouterLink to="/products" class="btn btn-primary">Volver a la tienda</RouterLink>
      </div>
    </div>
  </div>
  <Footer id="footer-bottom"/>
</template>

<style>

.card2 {
  margin-top: 20px;
  margin-bottom: 20px;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
}

</style>