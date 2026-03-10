import { defineStore } from "pinia";
import systemApi, {
    type EmulatorSchema,
    type BuildSchema,
} from "@/services/api/system";

export type Emulator = EmulatorSchema;
export type Build = BuildSchema;

export default defineStore("systems", {
    state: () => ({
        allEmulators: [] as Emulator[],
        allBuilds: [] as Build[],
        currentEmulator: null as Emulator | null,
        currentBuild: null as Build | null,
        filterText: "" as string,
        fetchingSystems: false as boolean,
    }),

    getters: {
        filteredEmulators: ({ allEmulators, filterText }) =>
            allEmulators
                .filter((e) =>
                    e.name.toLowerCase().includes(filterText.toLowerCase()),
                )
                .sort((a, b) => a.name.localeCompare(b.name)),
        filteredBuilds: ({ allBuilds, filterText }) =>
            allBuilds
                .filter((b) =>
                    b.name.toLowerCase().includes(filterText.toLowerCase()),
                )
                .sort((a, b) => a.name.localeCompare(b.name)),
    },

    actions: {
        async fetchSystems() {
            if (this.fetchingSystems) return;
            this.fetchingSystems = true;

            try {
                const emulatorsRes = await systemApi.getEmulators();
                this.allEmulators = emulatorsRes.data;
            } catch (error) {
                console.error("Failed to fetch emulators:", error);
            }

            try {
                const buildsRes = await systemApi.getBuilds();
                this.allBuilds = buildsRes.data;
            } catch (error) {
                console.error("Failed to fetch builds:", error);
            }

            this.fetchingSystems = false;
        },
        setCurrentEmulator(emulator: Emulator) {
            this.currentEmulator = emulator;
        },
        setCurrentBuild(build: Build) {
            this.currentBuild = build;
        },
        reset() {
            this.allEmulators = [];
            this.allBuilds = [];
            this.currentEmulator = null;
            this.currentBuild = null;
            this.filterText = "";
        },
    },
});
