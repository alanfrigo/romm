<script setup lang="ts">
import { storeToRefs } from "pinia";
import { onBeforeMount, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useDisplay } from "vuetify";
import systemApi from "@/services/api/system";
import storeSystems from "@/stores/systems";
import type { Build } from "@/stores/systems";

const route = useRoute();
const router = useRouter();
const { mdAndDown, mdAndUp, lgAndUp, smAndDown } = useDisplay();
const systemsStore = storeSystems();
const { currentBuild } = storeToRefs(systemsStore);

const loading = ref(false);
const notFound = ref(false);
const tab = ref<"details" | "screenshots">("details");
const editingSummary = ref(false);
const summaryText = ref("");

async function fetchDetails() {
  loading.value = true;
  const id = parseInt(route.params.id as string);
  try {
    const { data } = await systemApi.getBuild(id);
    currentBuild.value = data;
    summaryText.value = data.summary || "";
    document.title = `${data.name} | Systems | RomM`;
  } catch (error) {
    console.error(error);
    notFound.value = true;
  } finally {
    loading.value = false;
  }
}

async function saveSummary() {
  if (!currentBuild.value) return;
  try {
    const { data } = await systemApi.updateBuild({
      id: currentBuild.value.id,
      summary: summaryText.value,
    });
    currentBuild.value = data;
    editingSummary.value = false;
  } catch (error) {
    console.error(error);
  }
}

function cancelEditSummary() {
  summaryText.value = currentBuild.value?.summary || "";
  editingSummary.value = false;
}

function formatBytes(bytes: number): string {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

onBeforeMount(() => {
  fetchDetails();
});
</script>

<template>
  <!-- Loading -->
  <v-container v-if="loading" class="d-flex justify-center mt-16">
    <v-progress-circular indeterminate color="primary" size="64" />
  </v-container>

  <!-- Not found -->
  <v-container v-else-if="notFound" class="text-center mt-16">
    <v-icon size="80" color="grey">mdi-alert-circle-outline</v-icon>
    <h2 class="text-h5 mt-4">Build not found</h2>
    <v-btn class="mt-4" color="primary" @click="router.back()">Go back</v-btn>
  </v-container>

  <!-- Detail page -->
  <template v-else-if="currentBuild">
    <!-- Background header -->
    <div
      class="bg-toplayer"
      style="height: 250px; position: relative; overflow: hidden"
    >
      <v-img
        v-if="currentBuild.path_cover_large"
        :src="currentBuild.path_cover_large"
        cover
        style="opacity: 0.3; position: absolute; inset: 0"
      />
    </div>

    <v-row
      :class="{ 'justify-center px-6': mdAndDown, 'd-flex px-16': lgAndUp }"
      no-gutters
    >
      <!-- Left column: Cover -->
      <v-col
        :cols="mdAndDown ? 'auto' : undefined"
        :style="mdAndUp ? 'flex: 0 0 270px; width: 270px' : undefined"
      >
        <v-container
          :width="mdAndDown ? 270 : undefined"
          class="pa-0"
          style="margin-top: -230px"
        >
          <v-card rounded="lg" class="overflow-hidden">
            <v-img
              v-if="currentBuild.path_cover_large"
              :src="currentBuild.path_cover_large"
              :aspect-ratio="3 / 4"
              cover
            />
            <div
              v-else
              class="d-flex align-center justify-center bg-toplayer"
              :style="{ 'aspect-ratio': '3/4' }"
            >
              <v-icon size="80" color="grey">mdi-package-variant-closed</v-icon>
            </div>
          </v-card>
        </v-container>
      </v-col>

      <!-- Right column: Tabs -->
      <v-col class="flex-grow-1">
        <div :class="{ 'pl-4': mdAndUp }" style="margin-top: -180px">
          <h1 class="text-h4 font-weight-bold text-white">
            {{ currentBuild.name }}
          </h1>
          <span class="text-caption text-grey">
            {{ currentBuild.slug }}
          </span>
        </div>

        <v-row
          :class="{ 'px-4': mdAndUp, 'justify-center': smAndDown }"
          no-gutters
        >
          <v-tabs
            v-model="tab"
            slider-color="primary"
            :class="{ 'mt-4': smAndDown }"
          >
            <v-tab value="details">Details</v-tab>
            <v-tab
              v-if="currentBuild.merged_screenshots.length > 0"
              value="screenshots"
            >
              Screenshots
            </v-tab>
          </v-tabs>

          <v-col cols="12" class="px-1">
            <v-window v-model="tab" disabled class="py-2">
              <!-- Details tab -->
              <v-window-item value="details">
                <v-row no-gutters>
                  <v-col>
                    <!-- File info -->
                    <v-card class="mb-4 pa-4" rounded="lg" variant="outlined">
                      <div class="text-subtitle-2 mb-2">File Info</div>
                      <v-table density="compact">
                        <tbody>
                          <tr>
                            <td class="text-caption font-weight-bold">Name</td>
                            <td>{{ currentBuild.file_name }}</td>
                          </tr>
                          <tr>
                            <td class="text-caption font-weight-bold">Path</td>
                            <td>{{ currentBuild.file_path }}</td>
                          </tr>
                          <tr>
                            <td class="text-caption font-weight-bold">Size</td>
                            <td>
                              {{ formatBytes(currentBuild.file_size_bytes) }}
                            </td>
                          </tr>
                          <tr>
                            <td class="text-caption font-weight-bold">
                              Extension
                            </td>
                            <td>{{ currentBuild.file_extension || "—" }}</td>
                          </tr>
                        </tbody>
                      </v-table>
                    </v-card>

                    <!-- Description -->
                    <v-card class="mb-4 pa-4" rounded="lg" variant="outlined">
                      <div
                        class="d-flex align-center justify-space-between mb-2"
                      >
                        <div class="text-subtitle-2">Description</div>
                        <v-btn
                          v-if="!editingSummary"
                          icon
                          size="small"
                          variant="text"
                          @click="editingSummary = true"
                        >
                          <v-icon size="18">mdi-pencil</v-icon>
                        </v-btn>
                      </div>
                      <template v-if="editingSummary">
                        <v-textarea
                          v-model="summaryText"
                          auto-grow
                          variant="outlined"
                          density="compact"
                          rows="4"
                          hide-details
                        />
                        <div class="d-flex justify-end mt-2">
                          <v-btn
                            size="small"
                            variant="text"
                            class="mr-2"
                            @click="cancelEditSummary"
                          >
                            Cancel
                          </v-btn>
                          <v-btn
                            size="small"
                            color="primary"
                            @click="saveSummary"
                          >
                            Save
                          </v-btn>
                        </div>
                      </template>
                      <p v-else-if="currentBuild.summary" class="text-body-2">
                        {{ currentBuild.summary }}
                      </p>
                      <p v-else class="text-body-2 text-grey">
                        No description yet. Click the pencil to add one.
                      </p>
                    </v-card>
                  </v-col>
                </v-row>
              </v-window-item>

              <!-- Screenshots tab -->
              <v-window-item value="screenshots">
                <v-row>
                  <v-col
                    v-for="(screenshot, idx) in currentBuild.merged_screenshots"
                    :key="idx"
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-img :src="screenshot" cover rounded="lg" />
                  </v-col>
                </v-row>
              </v-window-item>
            </v-window>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </template>
</template>
