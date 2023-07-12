<template>
  <q-page class="flex flex-center">
    <q-list bordered separator>
      <q-item clickable v-ripple v-for="(device, index) in devices" :key="index" @click="navigateToDevice(device)">
        <q-item-section>{{ device['Node Name'] }}</q-item-section>
      </q-item>
    </q-list>

    <!-- Add the DeviceDetailPage component here -->
    <device-detail-page v-if="selectedDevice" :device="selectedDevice" />
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import DeviceDetailPage from 'components/DeviceDetailPage.vue'

export default defineComponent({
  name: 'IndexPage',
  data() {
    return {
      devices: [],
      selectedDevice: null // Track the selected device
    };
  },
  mounted() {
    console.log("index page mounted");
    // Connect to the Socket.IO server
    //this.$socketio.connect();

    // Listen for the connection event
    this.$socketio.on('update_list_devices', (data) => {
      this.devices = data.device;
      console.log("new update from server: ", data.device.system_information['Node Name']);
    });
  },
  methods: {
    navigateToDevice(device) {
      this.selectedDevice = device; // Set the selected device
    }
  },
  components: {
    DeviceDetailPage
  }
})
</script>
