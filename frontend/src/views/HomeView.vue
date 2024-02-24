<script setup>
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
import axios from 'axios';

// export const homeView = {
//   data() {
//     return {
//       imageUrl: 'http://localhost:5173/src/assets/background-panaderia.jpg',
//       products: []
//     };
//   },
//   methods: {
//     async fetchProducts() {
//       axios.get('http://localhost:8000/api/v1.0/products/')
//         .then(response => {
//           this.products.push(response.data)
//         })
//         .catch(error => {
//           console.log(error)
//         })
//     }
//   }
// };


const imageUrl = '../assets/background-panaderia.jpg'

const products = []

const fetchProducts = axios.get('http://localhost:8000/api/v1.0/products/')
  .then(response => {
    products.push(response.data)
  })
  .catch(error => {
    console.log(error)
  })

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
        <template v-for=" product in products" :key="product.id">
          <div class="container" style="width: 18rem; margin: 10px;">
            <img :src="product.image" alt="..."/>
            <div class="container">
              <h5>{{ product.name }}</h5>
              <p>{{ product.description }}</p>
            </div>
          </div>
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

</style>