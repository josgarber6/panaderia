<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import axios from 'axios';
import moment from 'moment';

export default {
  data() {
    return {
      orders: [],
    };
  },
  components: {
    Navbar,
    Footer,
  },
  methods: {
    getOrders() {
      axios.get(`${import.meta.env.VITE_APP_BASE_URL}orders/my_orders`).then((response) => {
        this.orders = response.data;
      });
    },
    formatDate(date) {
      return moment(date).format('DD/MM/YYYY HH:mm');
    },
  },
  created() {
    this.getOrders();
  },
};
</script>

<template>
  <Navbar />
  <div class="container">
    <h1 class="text-center">Mis pedidos</h1>
    <div v-if="orders.length === 0" class="container text-center" style="padding-top: 20px;">
      <h4>No hay pedidos</h4>
    </div>
    <div v-for="order in orders" :key="order.id" class="container" style="padding-top: 20px;">
      <div class="table-responsive">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Correo electrónico</th>
              <th>Dirección</th>
              <th>Código Postal</th>
              <th>Fecha de creación</th>
              <th>Estado</th>
              <th>Pagado</th>
              <th>Método de envío</th>  
              <th>Total</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <time :datetime="order.created">{{ formatDate(order.created) }}</time>
              <td>{{ order.status }}</td>
              <td>{{ order.total }}</td>
              <td>
                <button class="btn btn-primary">Ver</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- Aquí iría tu tabla de reclamaciones -->
      <table class="table table-striped">
        <!-- ... -->
      </table>
      <!-- Aquí iría tu tabla de items del pedido -->
      <table class="table table-striped">
        <!-- ... -->
      </table>
    </div>
  </div>
  <Footer id="footer-bottom"/>
</template>

<style>

</style>