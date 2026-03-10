<script setup lang="ts">
import { useActiveElement } from "@vueuse/core";
import { storeToRefs } from "pinia";
import { ref, watch, computed } from "vue";
import { useDisplay } from "vuetify";
import { useRouter } from "vue-router";
import storeNavigation from "@/stores/navigation";
import storeSystems from "@/stores/systems";
import { ROUTES } from "@/plugins/router";

const { mdAndUp, smAndDown } = useDisplay();
const activeElement = useActiveElement();
const router = useRouter();
const navigationStore = storeNavigation();
const systemsStore = storeSystems();
const { filteredEmulators, filteredBuilds, filterText } =
  storeToRefs(systemsStore);
const { activeSystemsDrawer } = storeToRefs(navigationStore);

const tabIndex = computed(() => (activeSystemsDrawer.value ? 0 : -1));

const triggerElement = ref<HTMLElement | null | undefined>(undefined);
watch(activeSystemsDrawer, (isOpen) => {
  if (isOpen) {
    triggerElement.value = activeElement.value;
    // Fetch systems when drawer opens
    systemsStore.fetchSystems();
  }
});

const clear = () => {
  filterText.value = "";
};

const onClose = () => {
  activeSystemsDrawer.value = false;
  triggerElement.value?.focus();
};

const navigateToEmulator = (id: number) => {
  router.push({ name: ROUTES.EMULATOR_DETAIL, params: { id } });
  activeSystemsDrawer.value = false;
};

const navigateToBuild = (id: number) => {
  router.push({ name: ROUTES.BUILD_DETAIL, params: { id } });
  activeSystemsDrawer.value = false;
};
</script>

<template>
  <v-navigation-drawer
    v-model="activeSystemsDrawer"
    mobile
    :location="smAndDown ? 'bottom' : 'left'"
    width="500"
    :class="{
      'my-2': mdAndUp || (smAndDown && activeSystemsDrawer),
      'ml-2': (mdAndUp && activeSystemsDrawer) || smAndDown,
      'drawer-mobile': smAndDown,
      'unset-height': mdAndUp,
    }"
    class="bg-surface pa-1"
    rounded
    :border="0"
    @update:model-value="clear"
    @keydown.esc="onClose"
  >
    <template #prepend>
      <v-text-field
        v-model="filterText"
        label="Search systems"
        :tabindex="tabIndex"
        aria-label="Search systems"
        prepend-inner-icon="mdi-filter-outline"
        variant="solo-filled"
        density="compact"
        single-line
        hide-details
        clearable
        @click:clear="clear"
      />
    </template>

    <v-expansion-panels class="mt-2" multiple flat variant="accordion">
      <!-- Emulators group -->
      <v-expansion-panel>
        <v-expansion-panel-title :tabindex="tabIndex" color="toplayer" static>
          <v-icon class="mr-2" size="small">mdi-controller</v-icon>
          Emulators ({{ filteredEmulators.length }})
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-list tabindex="-1" lines="two" class="py-1 px-0">
            <v-list-item
              v-for="emulator in filteredEmulators"
              :key="emulator.id"
              :tabindex="tabIndex"
              :aria-label="emulator.name"
              role="listitem"
              @click="navigateToEmulator(emulator.id)"
            >
              <template #prepend>
                <v-avatar size="40" rounded class="mr-3 bg-toplayer">
                  <v-img
                    v-if="emulator.path_cover_small"
                    :src="emulator.path_cover_small"
                    cover
                  />
                  <v-icon v-else>mdi-controller</v-icon>
                </v-avatar>
              </template>
              <v-list-item-title>{{ emulator.name }}</v-list-item-title>
              <v-list-item-subtitle>
                {{ emulator.file_name }}
              </v-list-item-subtitle>
            </v-list-item>
            <v-list-item v-if="filteredEmulators.length === 0">
              <v-list-item-title class="text-center text-caption">
                No emulators found
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-expansion-panel-text>
      </v-expansion-panel>

      <!-- Builds group -->
      <v-expansion-panel>
        <v-expansion-panel-title :tabindex="tabIndex" color="toplayer" static>
          <v-icon class="mr-2" size="small">mdi-package-variant-closed</v-icon>
          Builds ({{ filteredBuilds.length }})
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-list tabindex="-1" lines="two" class="py-1 px-0">
            <v-list-item
              v-for="build in filteredBuilds"
              :key="build.id"
              :tabindex="tabIndex"
              :aria-label="build.name"
              role="listitem"
              @click="navigateToBuild(build.id)"
            >
              <template #prepend>
                <v-avatar size="40" rounded class="mr-3 bg-toplayer">
                  <v-img
                    v-if="build.path_cover_small"
                    :src="build.path_cover_small"
                    cover
                  />
                  <v-icon v-else>mdi-package-variant-closed</v-icon>
                </v-avatar>
              </template>
              <v-list-item-title>{{ build.name }}</v-list-item-title>
              <v-list-item-subtitle>
                {{ build.file_name }}
              </v-list-item-subtitle>
            </v-list-item>
            <v-list-item v-if="filteredBuilds.length === 0">
              <v-list-item-title class="text-center text-caption">
                No builds found
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-navigation-drawer>
</template>
