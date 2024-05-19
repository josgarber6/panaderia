<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import axios from 'axios';
import { RouterLink } from 'vue-router';

export default {
  name: 'AdminEditProduct',
  components: {
    Navbar,
    Footer,
    RouterLink,
  },
  data() {
    return {
      product: {},
      categories: [],
      productId: this.$route.params.productId,
      selectedFile: null,
      windowWidth: 0,
      windowHeight: 0,
      showImage: true,
      message: '',
    };
  },
  methods: {
    getProduct() {
      axios.get(`${import.meta.env.VITE_APP_BASE_URL}products/${this.productId}/`)
        .then(response => {
          this.product = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    },
    getCategories() {
      axios.get(`${import.meta.env.VITE_APP_BASE_URL}categories/`)
        .then(response => {
          this.categories = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    },
    handleFileUpload(event) {
      const imageFile = event.target.files[0];
      const formData = new FormData();
      formData.append('image', imageFile);
      const csrf_token = document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];
      return axios.post(`${import.meta.env.VITE_APP_BASE_URL}products/check-image/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-CSRFToken': csrf_token,
        },
      })
        .then(response => {
          if (response.data.exists) {
            this.selectedFile = null;
            alert('Esta imagen ya existe en la base de datos, por favor, seleccione otra imagen');
          } else if (!response.data.exists && response.status === 200) {
            this.showImage = false;
            this.selectedFile = event.target.files[0];
          }
        })
        .catch(error => {
          if (error.response) {
            if (error.response.status === 400) {
              this.$refs.fileInput.value = '';
              this.message = error.response.data.detail;
            } else {
              console.log(error);
            }
          }
        });
    },
    updateProduct() {
      let formData = new FormData();
      Object.keys(this.product).forEach(key => {
        formData.append(key, this.product[key]);
      });
      if (this.selectedFile) {
        formData.append('image', this.selectedFile);
      } else {
        formData.append('image', this.product.image);
      }
      const csrf_token = document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];
      try {
        axios.put(`${import.meta.env.VITE_APP_BASE_URL}products/${this.productId}/`, formData, {
          headers: {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'multipart/form-data',
          },
        })
        .then((response) => {
          if (response.status === 200) {
            this.$store.commit('SET_ALERT_MESSAGE', 'Producto actualizado correctamente');
          }
          this.$router.push('/admin/products');
          })
        .catch((error) => {
          if (error.response) {
            if (error.response.status === 400 || error.response.status === 403) {
              this.message = error.response.data.detail;
            } else {
              console.log(error);
            }
          }
        });
      } catch (error) {
        console.log(error);
      }
    },
    handleResize() {
      this.windowWidth = window.innerWidth;
      this.windowHeight = window.innerHeight;
    },
  },
  created() {
    this.getProduct();
    this.getCategories();
    window.addEventListener('resize', this.handleResize);
    this.handleResize();
  },
};
</script>

<template>
  <Navbar />
  <div class="container mt-4">
    <div v-if="message" class="alert alert-danger">
      {{ message }}
    </div>
    <div class="column">
      <h3>Editar Producto</h3>
      <p>Los campos con un (<span class="is-required-note"/>) son obligatorios</p>
    </div>
    <div class="column">
      <div style="display: flex; flex-direction: column; justify-content: center;">
        <div class="form-group">
          <label for="name" class="is-required">Nombre</label>
          <input type="text" class="form-control" id="name" v-model="product.name">
        </div>
        <div class="form-group">
          <label for="description" class="is-required">Descripci&#243;n</label>
          <textarea class="form-control" id="description" v-model="product.description"></textarea>
        </div>
        <div class="form-group d-flex align-items-center">
          <label for="price" class="mr-2 is-required">Precio</label>
          <input type="number" class="form-control" id="price" v-model="product.price" min="0" style="width: fit-content;"><label style="margin-left: 5px;">€</label>
        </div>
        <div class="form-group d-flex align-items-center">
          <label for="stock" class="mr-2 is-required">Stock</label>
          <input type="number" class="form-control" id="stock" v-model="product.stock" style="width: fit-content;"><label style="margin-left: 5px;">unidades</label>
        </div>
        <div class="form-group">
          <label for="category" class="is-required">Categor&iacute;a</label>
          <select class="form-control" id="category" v-model="product.category">
            <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label for="highlighted" class="mr-2">Destacar</label>
          <input type="checkbox" id="highlighted" v-model="product.highlighted">
        </div>
        <div class="form-group">
          <label for="image">Imagen actual</label>
          <div style="display: flex; justify-content: center; flex-direction: column">
            <!-- Para evitar el problema de que no se pueda eliminar una imagen si se está usando
            utilizamos una condición que se modifica al cargar una imagen nueva -->
            <template v-if="showImage">
              <img :src="product.image" alt="Imagen del producto" style="width: 100px; height: 100px; margin-top: 10px;"/>
            </template>
            <input type="file" id="image" @change="handleFileUpload" ref="fileInput">
          </div>
        </div>
      </div>
      <div style="display: flex; justify-content: center; margin-top: 10px; margin-bottom: 20px;">
        <button class="btn btn-primary" @click="updateProduct" style="margin-right: 10px;">Actualizar</button>
        <RouterLink class="btn btn-danger" to="/admin/products">Cancelar</RouterLink>
      </div>
    </div>
  </div>
  <Footer/>
</template>

<style scoped>
</style>