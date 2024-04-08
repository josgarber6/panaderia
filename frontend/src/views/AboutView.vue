<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import sanchez from '@/assets/sanchez.jpeg';

export default {
  name: 'AboutView',
  data() {
    return {
      sanchez,
      isBodyTextHidden: false,
    }
  },
  components: {
    Navbar,
    Footer
  },
  mounted() {
    window.addEventListener('resize', this.handleResize);
    this.$nextTick(() => {
      this.handleResize();
    });
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    handleResize() {
      this.isBodyTextHidden = document.body.scrollHeight > window.innerHeight;
    }
  },
  created() {
    window.addEventListener('resize', this.handleResize);
    this.handleResize();
  },
}
</script>
<template>
  <Navbar />
  <div class="about">
    <h1 class="title">Acerca de Panader&iacute;a S&aacute;nchez</h1>
    <img :src="sanchez" alt="Imagen de la panadería" class="about-image">
    <p class="about-text">
      La empresa familiar Panadería Sánchez, fundada en la tradición panadera, que tiene una historia que se remonta a generaciones, 
      ha sido un pilar en la comunidad desde hace mucho tiempo, ofreciendo productos 
      horneados frescos y deliciosos con un toque casero inconfundible.
      <br><br>
      Panadería Sánchez inicia una nueva etapa de expansión y digitalización con la intención de atraer a más personas y compartir su amor por el arte de la panadería.

      La decisión tomada por la familia Sánchez muestra su compromiso con su legado y su anhelo de llegar a un público más amplio con sus productos. 
      Cada pieza de pan que sale del obrador se evalúa minuciosamente en términos de calidad y sabor, para que la experiencia gastronómica sea inolvidable.
    </p>
  </div>
  <Footer :id="isBodyTextHidden ? 'footer-bottom' : ''"/>
</template>

<style scoped>
.about {
  padding: 2em;
  text-align: justify;
}

.title {
  font-size: 2em;
  text-align: center;
  margin-bottom: 1em;
}

.about-text {
  font-size: 1.2em;
  line-height: 1.6;
  font-family: sans-serif;
}

.about-image {
  width: 300px;
  height: auto;
  margin-bottom: 1em;
  border-radius: 10px;
  justify-self: center;
}

.about {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>