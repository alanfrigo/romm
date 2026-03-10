<script setup lang="ts">
import { storeToRefs } from "pinia";
import { onBeforeMount } from "vue";
import { useDisplay } from "vuetify";
import { useRouter } from "vue-router";
import storeSystems from "@/stores/systems";
import { ROUTES } from "@/plugins/router";

const { mdAndUp, smAndDown } = useDisplay();
const router = useRouter();
const systemsStore = storeSystems();
const { filteredEmulators, filteredBuilds, fetchingSystems, filterText } =
  storeToRefs(systemsStore);

onBeforeMount(() => {
  document.title = "Systems | RomM";
  systemsStore.fetchSystems();
});

const navigateToEmulator = (id: number) => {
  router.push({ name: ROUTES.EMULATOR_DETAIL, params: { id } });
};

const navigateToBuild = (id: number) => {
  router.push({ name: ROUTES.BUILD_DETAIL, params: { id } });
};
</script>

<template>
  <v-container class="pa-4">
    <!-- Header -->
    <v-row class="mb-4" no-gutters>
      <v-col cols="12">
        <div class="d-flex align-center justify-space-between">
          <h1 class="text-h4 font-weight-bold">
            <v-icon class="mr-2" size="32">mdi-chip</v-icon>
            Systems
          </h1>
          <v-text-field
            v-model="filterText"
            class="ml-4"
            style="max-width: 300px"
            label="Search"
            prepend-inner-icon="mdi-magnify"
            variant="solo-filled"
            density="compact"
            single-line
            hide-details
            clearable
          />
        </div>
      </v-col>
    </v-row>

    <!-- Loading -->
    <v-row v-if="fetchingSystems" class="justify-center mt-8">
      <v-progress-circular indeterminate color="primary" />
    </v-row>

    <template v-else>
      <!-- Emulators section -->
      <v-row class="mb-2" no-gutters>
        <v-col cols="12">
          <h2 class="text-h6 font-weight-medium mb-3">
            <v-icon class="mr-1" size="20">mdi-controller</v-icon>
            Emulators ({{ filteredEmulators.length }})
          </h2>
        </v-col>
      </v-row>

      <v-row v-if="filteredEmulators.length > 0">
        <v-col
          v-for="emulator in filteredEmulators"
          :key="emulator.id"
          cols="12"
          sm="6"
          md="4"
          lg="3"
        >
          <v-card
            class="pa-0 cursor-pointer system-card"
            variant="outlined"
            rounded="lg"
            @click="navigateToEmulator(emulator.id)"
          >
            <v-img
              v-if="emulator.path_cover_small"
              :src="emulator.path_cover_small"
              height="160"
              cover
              class="bg-toplayer"
            />
            <div
              v-else
              class="d-flex align-center justify-center bg-toplayer"
              style="height: 160px"
            >
              <v-icon size="64" color="grey">mdi-controller</v-icon>
            </div>
            <v-card-title class="text-subtitle-1 font-weight-bold">
              {{ emulator.name }}
            </v-card-title>
            <v-card-subtitle v-if="emulator.summary" class="text-caption pb-3">
              {{ emulator.summary }}
            </v-card-subtitle>
          </v-card>
        </v-col>
      </v-row>
      <v-row v-else class="mb-4">
        <v-col cols="12">
          <v-alert type="info" variant="tonal" class="text-center">
            No emulators found
          </v-alert>
        </v-col>
      </v-row>

      <!-- Builds section -->
      <v-row class="mb-2 mt-6" no-gutters>
        <v-col cols="12">
          <h2 class="text-h6 font-weight-medium mb-3">
            <v-icon class="mr-1" size="20">mdi-package-variant-closed</v-icon>
            Builds ({{ filteredBuilds.length }})
          </h2>
        </v-col>
      </v-row>

      <v-row v-if="filteredBuilds.length > 0">
        <v-col
          v-for="build in filteredBuilds"
          :key="build.id"
          cols="12"
          sm="6"
          md="4"
          lg="3"
        >
          <v-card
            class="pa-0 cursor-pointer system-card"
            variant="outlined"
            rounded="lg"
            @click="navigateToBuild(build.id)"
          >
            <v-img
              v-if="build.path_cover_small"
              :src="build.path_cover_small"
              height="160"
              cover
              class="bg-toplayer"
            />
            <div
              v-else
              class="d-flex align-center justify-center bg-toplayer"
              style="height: 160px"
            >
              <v-icon size="64" color="grey">mdi-package-variant-closed</v-icon>
            </div>
            <v-card-title class="text-subtitle-1 font-weight-bold">
              {{ build.name }}
            </v-card-title>
            <v-card-subtitle v-if="build.summary" class="text-caption pb-3">
              {{ build.summary }}
            </v-card-subtitle>
          </v-card>
        </v-col>
      </v-row>
      <v-row v-else>
        <v-col cols="12">
          <v-alert type="info" variant="tonal" class="text-center">
            No builds found
          </v-alert>
        </v-col>
      </v-row>
    </template>
  </v-container>
</template>

<style scoped>
.system-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.system-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}
.cursor-pointer {
  cursor: pointer;
}
</style>
