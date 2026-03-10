<script setup lang="ts">
import { storeToRefs } from "pinia";
import { useI18n } from "vue-i18n";
import storeNavigation from "@/stores/navigation";

withDefaults(
  defineProps<{
    block?: boolean;
    height?: string;
    rounded?: boolean;
    withTag?: boolean;
  }>(),
  {
    block: false,
    height: "",
    rounded: false,
    withTag: false,
  },
);
const { t } = useI18n();
const navigationStore = storeNavigation();
const { activeSystemsDrawer } = storeToRefs(navigationStore);
</script>
<template>
  <v-btn
    icon
    :block="block"
    variant="flat"
    rounded="1"
    :height="height"
    class="py-4 bg-background d-flex align-center justify-center"
    :class="{ rounded: rounded }"
    :color="activeSystemsDrawer ? 'toplayer' : 'background'"
    @click="navigationStore.switchActiveSystemsDrawer"
  >
    <div class="d-flex flex-column align-center">
      <v-icon :color="$route.name == 'systems' ? 'primary' : ''">
        mdi-chip
      </v-icon>
      <v-expand-transition>
        <span
          v-if="withTag"
          class="text-caption text-center"
          :class="{ 'text-primary': $route.name == 'systems' }"
          >Systems</span
        >
      </v-expand-transition>
    </div>
  </v-btn>
</template>
