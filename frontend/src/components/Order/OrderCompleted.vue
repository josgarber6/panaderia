<script>
import { RouterLink } from 'vue-router';
import Navbar from '../Navbar.vue';
import Footer from '../Footer.vue';

export default {
  components: {
    Navbar,
    Footer,
    RouterLink,
  },
  computed: {
    orderId() {
      return sessionStorage.getItem('orderId');
    }
  },
};

</script>

<template>
  <Navbar />
  <div class="container mt-4">
    <div class="card2 text-center">
      <div class="card-body">
        <h1 class="card-title">¡Pedido realizado! El ID para el seguimiento de tu pedido es {{ orderId }}</h1>
        <p class="card-text"> Puedes consultar el estado de tu pedido en
          <RouterLink to="/order/my_orders">este enlace</RouterLink>.
        </p>
        <p class="card-text">Gracias por tu compra.</p>
        <p class="card-text">Recibirás un correo electrónico de confirmación pronto.</p>
        <RouterLink to="/products" class="btn btn-primary">Volver a la tienda</RouterLink>
      </div>
    </div>
  </div>
  <Footer id="footer-bottom"/>
</template>

<style scoped>

.card2 {
  margin-top: 20px;
  margin-bottom: 20px;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
}

</style>