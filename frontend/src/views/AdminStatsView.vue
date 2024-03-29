<script>
import axios from 'axios';
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';

export default {
  name: 'AdminStatsView',
  components: {
    Navbar,
    Footer,
  },
  data() {
    return {
      totalProducts: 0,
      totalUsers: 0,
      totalOrders: 0,
      topProducts: [],
      numTopProducts: 10,
      topUsers: [],
      numTopUsers: 2,
      errorMessage: '',
      loading: false,
      isBodyTextHidden: false,
    };
  },
  mounted() {
    Promise.all([
      axios.get(`${import.meta.env.VITE_APP_BASE_URL}products`).then((response) => {
        this.totalProducts = response.data.length;
      }),
      axios.get(`${import.meta.env.VITE_APP_BASE_URL}orders`).then((response) => {
        this.totalOrders = response.data.length;
      })
    ]).then(() => {
      window.addEventListener('resize', this.handleResize);
      this.$nextTick(() => {
        this.handleResize();
      });
    })
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    getProductInfo(productId) {
      return axios.get(`${import.meta.env.VITE_APP_BASE_URL}products/${productId}`);
    },
    async getTopProducts() {
      this.loading = true;
      try {
        const response = await axios.get(`${import.meta.env.VITE_APP_BASE_URL}orders`);
        const orders = response.data;
        const productCounts = {};
  
        // Contar el número de veces que se ha comprado cada producto en todos los pedidos
        for (const order of orders) {
          // Para cada pedido, recorre todos sus artículos
          for (const item of order.items) {
            // Si el producto ya existe en productCounts
            if (item.product in productCounts) {
              // Incrementa el conteo del producto por la cantidad del artículo
              productCounts[item.product].count += item.quantity;
            } else {
              // Si el producto no existe en productCounts, crea una nueva entrada
              // para el producto con el conteo inicializado a la cantidad del artículo
              productCounts[item.product] = {
                product: null,
                count: item.quantity,
              };
            }
          }
        }
        
        // Obtener la información de cada producto
        const productIds = Object.keys(productCounts);
        await Promise.all(productIds.map(async (productId) => {
          const productResponse = await this.getProductInfo(productId);
          productCounts[productId].product = productResponse.data;
        }));
        
        // Ordenar los productos por el número de veces que se han comprado
        this.topProducts = Object.values(productCounts)
        .sort((a, b) => b.count - a.count)
        .slice(0, this.numTopProducts);  // Top 10 products
      } catch (error) {
        if (error.response.status === 401) {
          this.errorMessage = 'Debe iniciar sesión y activar el doble factor de autenticación para ver las estadísticas.'
        } else if (error.response.status === 403) {
          this.errorMessage = 'Debe activar el doble factor de autenticación para ver las estadísticas.'
        } else {
          this.errorMessage = 'Ocurrió un error al cargar los productos.'
        }
      } finally {
        this.loading = false;
      }
    },
    getUserInfo(userId) {
      return axios.get(`${import.meta.env.VITE_APP_BASE_URL_SHORT}account/get-user-info/${userId}`);
    },
    async getTopUsers() {
      this.loading = true;
      try {
        const customersAPI = await axios.get(`${import.meta.env.VITE_APP_BASE_URL_SHORT}account/customers`)
        const customers = customersAPI.data;
        const userCounts = {};
  
        // Inicializar el conteo de pedidos para cada usuario
        for (const customer of customers) {
          userCounts[customer.user] = {
            user: null,
            count: 0,
          };
        }
        
        const ordersAPI = await axios.get(`${import.meta.env.VITE_APP_BASE_URL}orders`);
        const orders = ordersAPI.data;
        // Contar el número de pedidos para cada usuario
        for (const order of orders) {
          userCounts[order.customer].count += 1;
        }
  
        // Obtener la información de cada usuario
        const userIds = Object.keys(userCounts);
        await Promise.all(userIds.map(async (userId) => {
          const userResponse = await this.getUserInfo(userId);
          userCounts[userId].user = userResponse.data;
        }));
          
        this.topUsers = Object.values(userCounts)
        .sort((a, b) => b.count - a.count)
        .slice(0, this.numTopUsers);  // Top 10 users
      } catch {
        if (error.response.status === 401) {
          this.errorMessage = 'Debe iniciar sesión y activar el doble factor de autenticación para ver las estadísticas.'
        } else if (error.response.status === 403) {
          this.errorMessage = 'Debe activar el doble factor de autenticación para ver las estadísticas.'
        } else {
          this.errorMessage = 'Ocurrió un error al cargar los usuarios.'
        }
      } finally {
        this.loading = false;
      }
    },
    handleResize() {
      this.isBodyTextHidden = document.body.scrollHeight > window.innerHeight;
    }
  },
  async created() {
    setTimeout(() => {
      this.loading = false;
    }, await this.getTopProducts(), await this.getTopUsers());
    this.$store.dispatch('loadCategories');
  },
};

</script>

<template>
  <Navbar />
  <div class="container mt-4">
    <div v-if="errorMessage" class="container text-center" style="padding-top: 20px;">
      <h4 style="color: red;" id="error-message">{{ errorMessage }}</h4>
    </div>
    <div v-else>
      <div class="container mt-4">
        <h3>Productos Totales: {{ totalProducts }}</h3>
        <h3>Pedidos Totales: {{ totalOrders }}</h3>
      </div>
      <div class="container mt-4">
        <div style="display: flex; justify-content: center; flex-direction: row; margin-bottom: 20px;">
          <h2>Top Productos</h2>
        </div>
        <div v-if="loading" class="container text-center" style="padding-top: 20px;">
          <h4>Cargando datos...</h4>
          <div class="spinner-border" role="status"></div>
        </div>
        <div v-else-if="topProducts.length === 0" class="container text-center" style="padding-top: 20px;">
          <h4>No hay datos</h4>
        </div>
        <div class="table-responsive centered-table" style="overflow-x: scroll; scrollbar-width: none; width: fit-content;" v-if="!loading">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Categor&iacute;a</th>
                <th>Precio</th>
                <th>Stock</th>
                <th>Cantidad</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="productInfo in topProducts" :key="productInfo.product.id">
                <td>{{ productInfo.product.name }}</td>
                <td>{{ $store.getters.getCategoryName(productInfo.product.category) }}</td>
                <td>{{ productInfo.product.price }}</td>
                <td>{{ productInfo.product.stock }}</td>
                <td>{{ productInfo.count }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div style="display: flex; justify-content: center; flex-direction: row; margin-top: 20px; margin-bottom: 20px;">
          <h2>Top Usuarios</h2>
        </div>
        <div v-if="loading" class="container text-center" style="padding-top: 20px;">
          <h4>Cargando datos...</h4>
          <div class="spinner-border" role="status"></div>
        </div>
        <div v-else-if="topUsers.length === 0" class="container text-center" style="padding-top: 20px;">
          <h4>No hay datos</h4>
        </div>
        <div class="table-responsive centered-table" style="overflow-x: scroll; scrollbar-width: none; width: fit-content;" v-if="!loading">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Apellido(s)</th>
                <th>Correo</th>
                <th>Pedidos</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in topUsers" :key="item.id">
                <td>{{ item.user.first_name }}</td>
                <td>{{ item.user.last_name }}</td>
                <td>{{ item.user.email }}</td>
                <td>{{ item.count }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
  <Footer :id="isBodyTextHidden ? 'footer-bottom' : ''"/>
</template>

<style>
.centered-table {
  margin-left: auto;
  margin-right: auto;
}
</style>