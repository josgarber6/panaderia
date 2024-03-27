<script>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import axios from 'axios';
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
import star from '@/assets/star.png';

export default {

  components: {
    Navbar,
    Footer
  },

  data() {
    return {
      products: [],
      star,
      windowWidth: 0,
      message: '',
    };
  },

  computed: {
    cart() {
      return this.$store.state.cart;
    },
  },

  methods: {
    fetchProducts() {
      axios.get(`${import.meta.env.VITE_APP_BASE_URL}products/`)
        .then(response => {
          this.products = response.data
        })
        .catch(error => {
          console.log(error)
        })
    },
    addToCart(product) {
      const quantity = parseInt(document.getElementById(`quantity-${product.id}`).value);
      if (this.$store.getters.getCategoryName(product.category) === 'Pico') {
        if (product.stock < quantity) {
          alert('No hay suficiente stock');
          return;
        } else {
          this.$store.dispatch('addToCart', { product, quantity });
        }
      } else {
        this.$store.dispatch('addToCart', { product, quantity });
      }
    },
    removeFromCart(itemId) {
      this.$store.dispatch('removeFromCart', itemId);
    },
    handleResize() {
      this.windowWidth = window.innerWidth;
    },
  },
  created() {
    this.fetchProducts()
    this.$store.dispatch('loadCart')
    this.$store.dispatch('loadCategories');
    this.handleResize();
    window.addEventListener('resize', this.handleResize);
  },
};
</script>

<template>
  <main>
    <Navbar id="fix"/>
    <p v-if="message" style="color: green;">{{ message }}</p>
    <div id="home">
      <div class="container-fluid m-0 p-0">
        <div style="display: flex; flex-direction: column; text-align: center;" class="d-none d-lg-block">
          <h1 class="display-1" style="color: aliceblue; font-weight: 500;">¡Bienvenido a la Panader&#237;a S&#225;nchez!</h1>
          <h3 style="color: aliceblue; font-weight: 500; font-size: 4vh;">Siente el sabor de la tradici&#243;n</h3>
        </div>
        <div style="display: flex; flex-direction: column; text-align: center;" class="d-block d-lg-none">
          <h1 class="display-3" style="color: aliceblue; font-weight: 400;">¡Bienvenido a la Panader&#237;a S&#225;nchez!</h1>
          <h3 style="color: aliceblue; font-weight: 400; font-size: 4vh;">Siente el sabor de la tradici&#243;n</h3>
        </div>
        <div class="mx-auto" style="max-width: 50%;">
            <!-- Línea divisoria -->
            <hr class="border border-white"/>
        </div>
      </div>
    </div>
    <!-- Productos destacados -->
    <div class="container-fluid m-0 p-0">
      <template v-if="windowWidth >= 1500">
        <div style="display: flex; flex-direction: column; text-align: center; background-color: chocolate;">
          <h2 style="color: aliceblue; font-weight: 500; margin-top: 20px">PRODUCTOS DESTACADOS</h2>
        </div>
        <div style="display: flex; flex-direction: row; justify-content: center; background-color: chocolate; min-height: 30vh; overflow-x: scroll; scrollbar-width: none;">
          <template v-for="product in products" :key="product.id">
            <template v-if="product.highlighted">
              <div class="card-container" style="margin: 10px">
                <div class="card">
                  <div class="product-image" style="position: relative;">
                    <img :src="product.image" alt="Imagen no disponible" class="card-img-top" style="width: 18rem; height: 16rem;"/>
                    <img :src="star" alt="Estrella" class="star-image" style="position: absolute; top: 0; left: 0;"/>
                  </div>
                  <div class="card-body">
                    <h5 class="card-title">{{ product.name }} {{ $store.getters.getCategoryName(product.category) }}</h5>
                    <p class="card-text">{{ product.description }}</p>
                    <h6 class="mb-0">{{ product.price }} €</h6>
                    <template v-if="$store.getters.getCategoryName(product.category) == 'Pico'">
                      <template v-if="product.stock > 1">
                        <p>Quedan {{ product.stock }} en stock</p>
                      </template>
                      <template v-else>
                        <p>Queda {{ product.stock }} en stock</p>
                      </template>
                      <template v-if="product.stock > 0">
                        <div class="d-flex align-items-center gap-1">
                          <div class="check">&#10003;</div>
                          <h6 class="text-success mb-0">Disponible</h6>
                        </div>
                      </template>
                      <template v-else>
                        <div class="d-flex align-items-center gap-1">
                          <div class="unavailable">&#10007;</div>
                          <h6 class="text-danger mb-0">Agotado</h6>
                        </div>
                      </template>
                    </template>
                  </div>
                  <div class="d-flex justify-content-between">
                    <div class="input-group mt-2">
                      <label class="input-group-text"
                              for="quantity">Cantidad</label>
                      <input type="number" class="form-control" :id="`quantity-${product.id}`"
                              name="quantity" min="1" value="1">
                      <button @click="addToCart(product)" :id="`add-to-cart-${product.id}`" class="btn btn-success">Añadir</button>
                    </div>
                  </div>
                </div>
              </div>
            </template>
          </template>
        </div>
      </template>
      <template v-else>
        <div style="display: flex; flex-direction: row; justify-content: flex-start; background-color: chocolate; min-height: 30vh; overflow-x: scroll; scrollbar-width: none;">
          <template v-for="product in products" :key="product.id">
            <template v-if="product.highlighted">
              <div class="card-container" style="margin: 10px">
                <div class="card">
                  <div class="product-image" style="position: relative;">
                    <img :src="product.image" alt="Imagen no disponible" class="card-img-top" style="width: 18rem; height: 16rem;"/>
                    <img :src="star" alt="Estrella" class="star-image" style="position: absolute; top: 0; left: 0;"/>
                  </div>
                  <div class="card-body">
                    <h5 class="card-title">{{ product.name }} {{ $store.getters.getCategoryName(product.category) }}</h5>
                    <p class="card-text">{{ product.description }}</p>
                    <h6 class="mb-0">{{ product.price }} €</h6>
                    <template v-if="$store.getters.getCategoryName(product.category) == 'Pico'">
                      <template v-if="product.stock > 1">
                        <p>Quedan {{ product.stock }} en stock</p>
                      </template>
                      <template v-else>
                        <p>Queda {{ product.stock }} en stock</p>
                      </template>
                      <template v-if="product.stock > 0">
                        <div class="d-flex align-items-center gap-1">
                          <div class="check">&#10003;</div>
                          <h6 class="text-success mb-0">Disponible</h6>
                        </div>
                      </template>
                      <template v-else>
                        <div class="d-flex align-items-center gap-1">
                          <div class="unavailable">&#10007;</div>
                          <h6 class="text-danger mb-0">Agotado</h6>
                        </div>
                      </template>
                    </template>
                  </div>
                  <div class="d-flex justify-content-between">
                    <div class="input-group mt-2">
                      <label class="input-group-text"
                              for="quantity">Cantidad</label>
                      <input type="number" class="form-control" :id="`quantity-${product.id}`"
                              name="quantity" min="1" value="1">
                      <button @click="addToCart(product)" id="add-to-cart" class="btn btn-success">Añadir</button>
                    </div>
                  </div>
                </div>
              </div>
            </template>
          </template>
        </div>
      </template>

      <div style="display: flex; flex-direction: row; justify-content: center; background-color: chocolate; min-height: 10vh;">
        <div style="display: flex; flex-direction: column; align-items: center; text-align: center; color: aliceblue; font-size: 2vh; font-weight: 500;">
          <h3>¡Descubre m&#225;s productos en nuestra tienda!</h3>
          <h3>¡No te quedes sin probarlos!</h3>
          <a href="/products" class="btn btn-secondary" id="button">Ver m&#225;s</a>
        </div>
      </div>
    </div>
    <Footer/>
  </main>
</template>

<style>

#fix {
  position: fixed;
  z-index: 1;
  width: 100%;
}

#home {
  background-image: linear-gradient(rgba(0, 0, 0, 0.25), rgba(0, 0, 0, 0.25)), url('@/assets/background-panaderia.jpg');
  background-size: cover;
  background-repeat: no-repeat;
  /* background-attachment: fixed; */
  background-position: center;
  height: 100vh;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
}

#button {
  display: flex;
  flex-direction: column;
  justify-content: center;
  background-color: #6b4d1f;
  width: fit-content;
  height: fit-content;
  max-height: 5vh;
  margin-top: 5px;
  margin-bottom: 10px;
}

.card-container {
  width: 18rem;
  transition: transform 0.3s ease-in-out;
  margin-bottom: 20px;
}

.card {
  border: none;
  border-radius: 8px;
  background-color: aliceblue;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
}

.card:hover {
  transform: translateY(-5px);
}

.card-img-top {
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
}

.check{
  width: 15px;
  height: 15px;
  border-radius: 50%;
  background-color: green;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.unavailable {
    width: 15px;
    height: 15px;
    border-radius: 50%;
    background-color: red;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
  }

.star-image {
  width: 70px;
  height: 70px;
}


</style>
