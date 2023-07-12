<template>
    <q-page>
      <h1>{{ device.name }}</h1>
      <p>Device IP: {{ device.System }}</p>
      <p>Device MAC: {{ device.mac }}</p>
      <!-- Add more details or customize the layout as needed -->
    </q-page>
  </template>
  
  <script>
  import { defineComponent } from 'vue'
  
  export default defineComponent({
    name: 'DeviceDetailPage',
    props: {
      device: {
        type: Object,
        required: true
      }
    }
  })
  </script>
  