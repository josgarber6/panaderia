<script>
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
import axios from 'axios';
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default {

  components: {
    Navbar,
    Footer
  },

  data() {
    return {
      imageUrl: 'http://localhost:5173/src/assets/background-panaderia.jpg',
      products: [],
      stock: true
    };
  },
  methods: {
    fetchProducts() {
      axios.get('http://localhost:8000/api/v1.0/products/')
        .then(response => {
          this.products = response.data
        })
        .catch(error => {
          console.log(error)
        })
    },

    stockStatus() {
      if (this.products.stock > 0) {
        this.stock = true
      } else {
        this.stock = false
      }
    }
  },
  created() {
    this.fetchProducts()

  },
};
</script>

<template>
  <main>
    <Navbar id="fix"/>
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
      <div style="display: flex; flex-direction: row; justify-content: center; background-color: chocolate; min-height: 30vh">
        <template v-for="product in products" :key="product.id">
          <template v-if="product.highlighted">
            <div class="card-container" style="margin: 10px;">
              <div class="card">
                <img :src="product.image" alt="Imagen no disponible" class="card-img-top"/>
                <div class="card-body">
                  <h5 class="card-title">{{ product.name }}</h5>
                  <p class="card-text">{{ product.description }}</p>
                  <div class="d-flex justify-content-between">
                    <h6 class="mb-0">{{ product.price }} €</h6>
                    <template v-if=stock>
                      <div class="d-flex align-items-center gap-1">
                        <div class="check">&#10003;</div>
                        <h6 class="text-success mb-0">Disponible</h6>
                      </div>
                    </template>
                    <template v-else>
                      <div class="d-flex align-items-center gap-1">
                        <i class="fas fa-times-circle text-danger"></i>
                        <h6 class="text-danger mb-0">Agotado</h6>
                      </div>
                    </template>
                  </div>
                  <form class="add-to-cart-form mt-3" action="{% url 'cart:cart_add' product.id %}" method="post">
                    <div class="d-flex justify-content-between">
                      <div class="input-group mt-2">
                        <label class="input-group-text"
                                for="quantity_{{ product.id }}">Cantidad</label>
                        <input type="number" class="form-control" id="quantity_{{ product.id }}"
                                name="quantity" min="1" value="1">
                      </div>
                      <button type="submit" class="btn btn-success mt-2">Añadir</button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </template>
        </template>

      </div>
      <div style="display: flex; flex-direction: row; justify-content: center; background-color: chocolate; min-height: 10vh;">
        <div style="display: flex; flex-direction: column; align-items: center; text-align: center; color: aliceblue; font-size: 2vh; font-weight: 500;">
          <h3>¡Descubre m&#225;s productos en nuestra tienda!</h3>
          <h3>¡No te quedes sin probarlos!</h3>
          <!-- <div style="display: flex; flex-direction: column; justify-content: center;"> -->
            <a href="/products" class="btn btn-secondary" id="button">Ver m&#225;s</a>
          <!-- </div> -->
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
  background-image: linear-gradient(rgba(0, 0, 0, 0.25), rgba(0, 0, 0, 0.25)), url('../assets/background-panaderia.jpg');
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


</style>