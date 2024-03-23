<script>
import axios from 'axios';
import moment from 'moment';

export default {
  data() {
    return {
      orders: [],
      customer: null,
      products: {},
      loading: false,
    };
  },
  methods: {
    async getOrders() {
      this.loading = true;
      const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL}orders/my_orders`)
      this.orders = response.data;

      for (const order of this.orders) {
        for (const item of order.items) {
          const product = await this.getProductInfo(item.product);
          this.products[item.product] = product;
        }
      }
      this.loading = false;
    },
    getCustomerInfo(customerId) {
      axios.get(`${import.meta.env.VITE_APP_BASE_URL_SHORT}account/customers/${customerId}`).then((response) => {
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
    setTimeout(() => {
      this.loading = false;
    }, await this.getOrders());
    if (this.orders.length > 0) {
      this.getCustomerInfo(this.orders[0].customer);
      this.$store.dispatch('loadCategories');
    }
  },
};
</script>

<template>
  <div class="container">
    <h1 class="text-center">Mis pedidos</h1>
    <div v-if="loading" class="container text-center" style="padding-top: 20px;">
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
              <td>{{ products[item.product].name }}</td>
              <td>{{ $store.getters.getCategoryName(products[item.product].category) }} </td>
              <td>{{ item.quantity }}</td>
              <td>{{ item.price }}</td>
              <td>{{ (item.quantity * item.price).toFixed(2) }} €</td>
            </tr>
          </tbody>
        </table>
      </div>
      <hr style="border: 1px solid #ccc;">
      <div style="padding: 10px;"></div>
    </div>
  </div>
</template>

<style>

th {
  font-weight: bold;
}

</style>