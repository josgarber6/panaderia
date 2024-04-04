<script>
import axios from 'axios';
import moment from 'moment';
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';

export default {
  data() {
    return {
      customer: null,
      products: {},
      loading: false,
      errorMessage: '',
      orders: [],
    };
  },
  components: {
    Navbar,
    Footer,
  },
  methods: {
    async getOrders() {
      this.loading = true;
      try {
        if (!this.$store.state.authenticated) {
          this.errorMessage = 'Debe iniciar sesión y activar el doble factor de autenticación para ver sus pedidos.'
          return;
        }
        const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL}orders/my_orders`)
        this.orders = response.data;

        // Obtener la información de los productos de cada pedido
        for (const order of this.orders) {
          for (const item of order.items) {
            const product = await this.getProductInfo(item.product);
            this.products[item.product] = product;
          }
        }
      } catch (error) {
        if (error.response.status === 401) {
          this.errorMessage = 'Debe iniciar sesión y activar el doble factor de autenticación para ver sus pedidos.'
        } else if (error.response.status === 403) {
          this.errorMessage = 'Debe activar el doble factor de autenticación para ver sus pedidos.'
        } else {
          this.errorMessage = 'Ocurrió un error al cargar los pedidos.'
        }
      } finally {
        this.loading = false;
      }
    },
    async getCustomerInfo(customerId) {
      await axios.get(`${import.meta.env.VITE_APP_BASE_URL_SHORT}account/customers/${customerId}`).then((response) => {
        this.customer = response.data;
      });
    },
    async getProductInfo(productId) {
      const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL}products/${productId}`)
      return response.data;
    },
    formatDate(date) {
      return moment(date).format('DD/MM/YYYY HH:mm');
    },
  },
  async created() {
    // Mostrar el spinner de carga hasta que se carguen los pedidos
    setTimeout(() => {
      this.loading = false;
    }, await this.getOrders());

    // Obtenemos la información del usuario asociado a los pedidos, que en este caso es la misma para todos los pedidos
    if (this.orders.length > 0) {
      await this.getCustomerInfo(this.orders[0].customer);
      this.$store.dispatch('loadCategories');
    }
  },
};
</script>

<template>
  <Navbar />
  <div class="container">
    <h1 class="text-center">Mis pedidos</h1>
    <div v-if="errorMessage" class="container text-center" style="padding-top: 20px;">
      <h4 style="color: red;" id="error-message">{{ errorMessage }}</h4>
    </div>
    <div v-else-if="loading" class="container text-center" style="padding-top: 20px;">
      <h4>Cargando pedidos...</h4>
      <div class="spinner-border" role="status"></div>
    </div>
    <div v-else-if="orders.length === 0" class="container text-center" style="padding-top: 20px;">
      <h4>No hay pedidos</h4>
    </div>
    <div v-for="order in orders" :key="order.id" class="container" style="padding-top: 20px;">
      <h3>Pedido {{ order.id }}</h3>
      <div class="table-responsive" style="overflow-x: scroll; scrollbar-width: none;">
        <table class="table table-striped">
          <template v-if="customer">
            <thead>
              <tr>
                <th>Dirección</th>
                <th>Código Postal</th>
                <th>Fecha de creación</th>
                <th>Estado</th>
                <th>Pagado</th>
                <th>Método de envío</th>
                <th>Método de pago</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{{ customer.address }}</td>
                <td>{{ customer.postal_code }}</td>
                <td>
                  <time :datetime="order.created">{{ formatDate(order.created) }}</time>
                </td>
                <td>{{ order.shipping_status }}</td>
                <template v-if="order.paid">
                  <td>Sí</td>
                </template>
                <template v-else>
                  <td>No</td>
                </template>
                <td>{{ order.shipping_method }}</td>
                <td>{{ order.payment_method }}</td>
                <td>{{ order.total_cost.toFixed(2) }} €</td>
              </tr>
            </tbody>
          </template>
        </table>
      </div>
      <div style="padding: 5px;"></div>
      <div class="table-responsive" style="overflow-x: scroll; scrollbar-width: none;">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Producto</th>
              <th>Categoría</th>
              <th>Cantidad</th>
              <th>Precio</th>
              <th>Subtotal</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in order.items" :key="item.id">
              <template v-if="products[item.product]">
                <td>{{ products[item.product].name }}</td>
                <td>{{ $store.getters.getCategoryName(products[item.product].category) }} </td>
                <td>{{ item.quantity }}</td>
                <td>{{ item.price }}</td>
                <td>{{ (item.quantity * item.price).toFixed(2) }} €</td>
              </template>
            </tr>
          </tbody>
        </table>
      </div>
      <hr style="border: 1px solid #ccc;">
      <div style="padding: 10px;"></div>
    </div>
  </div>
  <template v-if="orders.length === 0">
    <Footer id="footer-bottom"/>
  </template>
  <template v-else>
    <Footer/>
  </template>
</template>

<style>

th {
  font-weight: bold;
}

</style>