<script>
import { Chart, BarElement, BarController, CategoryScale, LinearScale } from 'chart.js';
import { ref, onMounted, watch, nextTick } from 'vue';

Chart.register(BarElement, BarController, CategoryScale, LinearScale);

export default {
  props: ['chartData', 'options'],
  setup(props) {
    const chartRef = ref(null);
    let chart = null;

    const renderChart = () => {
      if (chart) {
        chart.destroy();
      }
      if (chartRef.value && props.chartData) {
        chart = new Chart(chartRef.value, {
          type: 'bar',
          data: props.chartData,
          options: props.options
        });
      }
    }

    watch(() => props.chartData, () => {
      nextTick(renderChart);
    }, { immediate: true });

    onMounted(() => {
      nextTick(renderChart);
    });

    return {
      chartRef
    }
  }
}
</script>

<template>
  <div class="chart-container">
    <canvas ref="chartRef"></canvas>
  </div>
</template>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  height: 100%;
}
</style>