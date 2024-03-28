<script>
import axios from 'axios';
import moment from 'moment';
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import lupa from '@/assets/lupa.png';

export default {
  data() {
    return {
      orders: [],
      customers: {},
      products: {},
      loading: false,
      errorMessage: '',
      currentPage: 1,
      ordersPerPage: 5,
      searchTerm: '',
      lupa
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
          this.errorMessage = 'Debe iniciar sesión y activar el doble factor de autenticación para ver los pedidos.'
          return;
        }
        const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL}orders/`)
        this.orders = response.data;

        // Obtenemos la información de los clientes y Pedidos de cada pedido al mismo tiempo
        await Promise.all(this.orders.map(async (order) => {
          const [customer, ...products] = await Promise.all([
            this.getCustomerInfo(order.customer),
            ...order.items.map((item) => this.getProductInfo(item.product)),
          ]);

          const user = await this.getUserInfo(customer.user);
          customer.user = user;
          this.customers[order.customer] = customer;
          order.items.forEach((item, index) => {
            this.products[item.product] = products[index];
          });
        }));

      } catch (error) {
        if (error.response.status === 401) {
          this.errorMessage = 'Debe iniciar sesión y activar el doble factor de autenticación para ver los pedidos.'
        } else if (error.response.status === 403) {
          this.errorMessage = 'Debe activar el doble factor de autenticación para ver los pedidos.'
        } else {
          this.errorMessage = 'Ocurrió un error al cargar los pedidos.'
        }
      } finally {
        this.loading = false;
      }
    },
    async getCustomerInfo(customerId) {
      const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL_SHORT}account/customers/${customerId}`);
      return response.data;
    },
    async getUserInfo(userId) {
      const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL_SHORT}account/get-user-info/${userId}`);
      return response.data;
    },
    async getProductInfo(orderId) {
      const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL}products/${orderId}`)
      return response.data;
    },
    nextPage() {
      if (this.currentPage * this.ordersPerPage < this.orders.length) {
        this.currentPage++;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    getPaginatedOrders() {
      const start = (this.currentPage - 1) * this.ordersPerPage;
      return this.filteredOrders.slice(start, start + this.ordersPerPage);
    },
    formatDate(date) {
      return moment(date).format('DD/MM/YYYY HH:mm');
    },
    showPermissionMessage(orderId=null, path=null, action=null) {
      if (this.$store.state.user.isTwoFactorEnabled) {
        if (action === 'delete') {
          if (confirm('¿Estás seguro de que quieres eliminar este pedido?')) {
            axios.delete(`${import.meta.env.VITE_APP_BASE_URL}orders/${orderId}/`, {
              headers: {
                'X-CSRFToken': document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1],
              },
            })
              .then((response) => {
                if (response.status === 204) {
                  this.$store.commit('SET_ALERT_MESSAGE', 'Pedido eliminado correctamente');
                }
                this.getOrders();
              })
              .catch(error => {
                console.log(error);
              });
          }
        } else if (action === 'edit') {
          this.$router.push(`${path}${orderId}/edit`);
        } else {
          this.$router.push(path);
        }
      } else {
        alert('Necesitas tener habilitado el doble factor de autenticación para realizar esta acción');
      }
    },
    clearAlertMessage() {
      setTimeout(() => {
        this.$store.commit('SET_ALERT_MESSAGE', null);
      }, 5000);
    },
  },
  async created() {
    setTimeout(() => {
      this.loading = false;
    }, await this.getOrders());
    if (this.orders.length > 0) {
      this.$store.dispatch('loadCategories');
    }
    this.clearAlertMessage();
  },
  computed: {
    // Filtramos los pedidos por nombre, apellido o ID de pedido
    // no es necesario que se declare en data porque no se va a modificar
    filteredOrders() {
      return this.orders.filter(order => {
        const customer = this.customers[order.customer];
        if (customer && customer.user) {
          return customer.user.first_name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
            customer.user.last_name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
            order.id.toString().includes(this.searchTerm.toLowerCase());
        }
        return false;
      });
    },
  },
};
</script>

<template>
  <Navbar/>
  <div class="container mt-4">
    <div style="display: flex; margin-bottom: 20px;">
      <input v-model="searchTerm" type="text" class="form-control" placeholder="Buscar por nombre, apellido o ID de pedido" style="width: 360px;"/>
      <img :src="lupa" alt="lupa" style="width: 20px; height: 20px; margin-left: -30px; margin-top: 10px;"/>
    </div>
    <div v-if="$store.state.alertMessage" class="alert alert-success">
      {{ $store.state.alertMessage }}
    </div>
    <h1 class="text-center">Pedidos</h1>
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
    <div v-else-if="filteredOrders.length === 0" class="container text-center" style="padding-top: 20px;">
      <h4>No se encontraron pedidos</h4>
    </div>
    <div v-for="order in getPaginatedOrders()" :key="order.id" class="container" style="padding-top: 20px;">
      <h2 v-if="customers[order.customer] && customers[order.customer].user">
        {{ customers[order.customer].user.first_name }} {{ customers[order.customer].user.last_name }}
      </h2>
      <div style="display: flex; justify-content: flex-start;">
        <h3>Pedido {{ order.id }}</h3>
        <button class="btn btn-primary" @click="showPermissionMessage(order.id, '/admin/orders/', 'edit')" 
        style="margin-left: 10px; margin-right: 5px; height: fit-content;">Editar</button>
        <button class="btn btn-danger" @click="showPermissionMessage(order.id, '/admin/orders/', 'delete')" 
        style="height: fit-content;">Eliminar</button>
      </div>
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
              <td>{{ customers[order.customer].address }}</td>
              <td>{{ customers[order.customer].postal_code }}</td>
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
    <div class="container d-flex justify-content-center align-items-center" style="margin-bottom: 20px;">
      <button class="btn btn-secondary" @click="prevPage" :disabled="currentPage === 1" style="margin-right: 10px;">Anterior</button>
      <button class="btn btn-secondary" @click="nextPage" :disabled="currentPage * ordersPerPage >= orders.length">Siguiente</button>
    </div>
  </div>
  <Footer v-if="searchTerm && filteredOrders.length === 0" id="footer-bottom"/>
  <Footer v-else-if="orders.length > 0"/>
  <Footer v-else id="footer-bottom"/>
  </template>

<style>

th {
  font-weight: bold;
}

</style>