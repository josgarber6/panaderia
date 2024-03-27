<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import axios from 'axios';

export default {
  name: 'AdminEditProduct',
  components: {
    Navbar,
    Footer,
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
      return axios.post(`${import.meta.env.VITE_APP_BASE_URL}products/check-image/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-CSRFToken': document.cookie.split('=')[1],
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
      const csrf_token = document.cookie.split('=')[1];
      try {
        axios.put(`${import.meta.env.VITE_APP_BASE_URL}products/${this.productId}/`, formData, {
          headers: {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'multipart/form-data',
          },
        })
        .then((response) => {
          if (response.status === 200) {
            this.$store.commit('SET_PRODUCT_ALERT_MESSAGE', 'Producto actualizado correctamente');
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
    </div>
    <div class="column">
      <div style="display: flex; flex-direction: column; justify-content: center;">
        <div class="form-group">
          <label for="name">Nombre</label>
          <input type="text" class="form-control" id="name" v-model="product.name">
        </div>
        <div class="form-group">
          <label for="description">Descripci&#243;n</label>
          <textarea class="form-control" id="description" v-model="product.description"></textarea>
        </div>
        <div class="form-group d-flex align-items-center">
          <label for="price" class="mr-2">Precio</label>
          <input type="number" class="form-control" id="price" v-model="product.price" style="width: fit-content;"><label style="margin-left: 5px;">€</label>
        </div>
        <div class="form-group d-flex align-items-center">
          <label for="stock" class="mr-2">Stock</label>
          <input type="number" class="form-control" id="stock" v-model="product.stock" style="width: fit-content;"><label style="margin-left: 5px;">unidades</label>
        </div>
        <div class="form-group">
          <label for="category">Categor&#237;a</label>
          <select class="form-control" id="category" v-model="product.category">
            <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
          </select>
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
  <!-- Si nos encontramos ante una pantalla más o menos pequeña en cuanto a altura y/o anchura, el footer se va a mostrar abajo
  sin entorpecer a los botones de Acutalizar y cancelar
  Se ha probado con una pantalla de 1536 x 703 px y en una pantalla de 1920 x 919 px -->
  <Footer id="footer-bottom" v-if="windowWidth >= 1920 || windowHeight >= 900"/>
  <Footer v-else/>
</template>

<style scoped>
</style>