<script>
export default {
  data() {
    return {
      payment_method: 'Tarjeta',
      shipping_method: 'Entrega estándar',
    };
  },
  methods: {
    confirmOrder() {
      this.$emit('confirm', {
        payment_method: this.payment_method,
        shipping_method: this.shipping_method,
      });
    },
    cancel() {
      this.$emit('cancel');
    },
  }
};
</script>
<template>
  <div class="overlay">
    <div id="modal">
      <h2>Selecciona el tipo de pago y entrega</h2>
      <div style="display: flex; justify-content: center; flex-direction: row;">
          <label for="payment" style="margin-right: 10px;">Tipo de Pago:</label>
          <select id="payment" v-model="payment_method">
            <option value="Tarjeta">Tarjeta de Crédito</option>
            <option value="Contra-reembolso">Pago en Efectivo</option>
          </select>
      </div>
      <div style="display: flex; justify-content: center; flex-direction: row;">
        <label for="shipping" style="margin-right: 10px;">Tipo de Entrega:</label>
        <select id="shipping" v-model="shipping_method">
          <option value="Entrega estándar">Entrega estándar</option>
          <option value="Recogida en tienda">Recogida en tienda</option>
        </select>
      </div>
      <div style="display: flex; justify-content: center; flex-direction: row;">
        <button class="btn btn-success" @click="confirmOrder">Confirmar Pedido</button>
        <button class="btn btn-danger" @click="cancel">Cancelar</button>
      </div>
    </div>
  </div>
</template>


<style>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* Fondo gris difuminado */
  display: flex;
  justify-content: center;
  align-items: center;
}

#modal {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
}

#modal h2 {
  margin-bottom: 10px;
}

#modal div {
  margin-bottom: 10px;
}

#modal button {
  margin-right: 10px;
}
</style>
