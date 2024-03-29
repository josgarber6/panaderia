<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import axios from 'axios';
import { RouterLink } from 'vue-router';

export default {
  name: 'AdminCreateProduct',
  components: {
    Navbar,
    Footer,
    RouterLink,
  },
  data() {
    return {
      product: {
        name: '',
        description: '',
        price: null,
        stock: null,
        category: 1,
        image: null,
      },
      windowWidth: 0,
      windowHeight: 0,
      categories: [],
      selectedFile: null,
      // mensaje de error si los hay
      message: '',
    };
  },
  methods: {
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
      // Gestionar la subida de la imagen
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
            this.$refs.fileInput.value = '';
          } else if (!response.data.exists && response.status === 200) {
            this.selectedFile = event.target.files[0];
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
    createProduct() {
      // Creamos un objeto FormData para enviar los datos del producto y la imagen
      const formData = new FormData();
      if (this.selectedFile) {
        formData.append('image', this.selectedFile);
      }
      for (let key in this.product) {
        formData.append(key, this.product[key]);
      }
      const csrf_token = document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];
      try {
        return axios.post(`${import.meta.env.VITE_APP_BASE_URL}products/`, formData, {
          headers: {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'multipart/form-data',
          },
          })
          .then((response) => {
          if (response.status === 201) {
            // Mostramos un mensaje de éxito, cuya configuración se encuentra en el store.js
            this.$store.commit('SET_ALERT_MESSAGE', 'Producto creado correctamente');
          }
          // Redirigimos a la vista de productos
          this.$router.push('/admin/products');
          })
          .catch((error) => {
            if (error.response) {
              if (error.response.status === 400 || error.response.status === 403) {
                this.message = error.response.data.detail;
              } else if (error.response && error.response.status === 500) {
                this.message = 'Ha ocurrido un error al crear el producto';
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
      <h3>Crear Producto</h3>
    </div>
    <div class="column">
      <div style="display: flex; flex-direction: column; justify-content: center;">
        <div class="form-group">
          <label for="name">Nombre</label>
          <input type="text" class="form-control" id="name" placeholder="Mollete" v-model="product.name">
        </div>
        <div class="form-group">
          <label for="description">Descripci&oacute;n</label>
          <textarea class="form-control" id="description" placeholder="Hecho con harina española" v-model="product.description"></textarea>
        </div>
        <div class="form-group d-flex align-items-center">
          <label for="price" class="mr-2">Precio</label>
          <input type="number" class="form-control" id="price" placeholder="0,8" v-model="product.price" style="width: fit-content;"><label style="margin-left: 5px;">€</label>
        </div>
        <div class="form-group d-flex align-items-center">
          <label for="stock" class="mr-2">Stock</label>
          <input type="number" class="form-control" id="stock" min="0" placeholder="50" v-model="product.stock" style="width: fit-content;"><label style="margin-left: 5px;">unidades</label>
        </div>
        <div class="form-group">
          <label for="category">Categor&iacute;a</label>
          <select class="form-control" id="category" v-model="product.category">
            <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label for="highlighted" class="mr-2">Destacar</label>
          <input type="checkbox" id="highlighted" v-model="product.highlighted">
        </div>
        <div class="form-group">
          <label for="image">Imagen</label>
          <!-- Utilizamos file input para no seleccionar la imagen en caso de que no sea válida -->
          <div style="display: flex; justify-content: center; flex-direction: column">
            <input type="file" id="image" @change="handleFileUpload" ref="fileInput">
          </div>
        </div>
      </div>
      <div style="display: flex; justify-content: center; margin-top: 20px; margin-bottom: 20px;">
        <button class="btn btn-primary" @click="createProduct" style="margin-right: 10px;">Crear</button>
        <RouterLink class="btn btn-danger" to="/admin/products">Cancelar</RouterLink>
      </div>
    </div>
  </div>
  <!-- Si nos encontramos ante una pantalla más o menos pequeña en cuanto a altura y/o anchura, el footer se va a mostrar abajo
  sin entorpecer a los botones de Actualizar y cancelar
  Se ha probado con una pantalla de 1536 x 703 px y en una pantalla de 1920 x 919 px -->
  <Footer id="footer-bottom" v-if="windowWidth >= 1920 || windowHeight >= 900"/>
  <Footer v-else/>
</template>

<style scoped>
</style>