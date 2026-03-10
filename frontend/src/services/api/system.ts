import api from "@/services/api";

export interface EmulatorSchema {
    id: number;
    name: string;
    slug: string;
    file_name: string;
    file_name_no_tags: string;
    file_name_no_ext: string;
    file_extension: string;
    file_path: string;
    file_size_bytes: number;
    summary: string | null;
    path_cover_small: string;
    path_cover_large: string;
    merged_screenshots: string[];
    platform_ids: number[];
    missing_from_fs: boolean;
    created_at: string;
    updated_at: string;
}

export interface BuildSchema {
    id: number;
    name: string;
    slug: string;
    file_name: string;
    file_name_no_tags: string;
    file_name_no_ext: string;
    file_extension: string;
    file_path: string;
    file_size_bytes: number;
    summary: string | null;
    path_cover_small: string;
    path_cover_large: string;
    merged_screenshots: string[];
    missing_from_fs: boolean;
    created_at: string;
    updated_at: string;
}

async function getEmulators() {
    return api.get<EmulatorSchema[]>("/systems/emulators");
}

async function getEmulator(id: number) {
    return api.get<EmulatorSchema>(`/systems/emulators/${id}`);
}

async function updateEmulator({
    id,
    summary,
}: {
    id: number;
    summary?: string;
}) {
    return api.put<EmulatorSchema>(`/systems/emulators/${id}`, { summary });
}

async function deleteEmulator(id: number) {
    return api.delete(`/systems/emulators/${id}`);
}

async function getBuilds() {
    return api.get<BuildSchema[]>("/systems/builds");
}

async function getBuild(id: number) {
    return api.get<BuildSchema>(`/systems/builds/${id}`);
}

async function updateBuild({
    id,
    summary,
}: {
    id: number;
    summary?: string;
}) {
    return api.put<BuildSchema>(`/systems/builds/${id}`, { summary });
}

async function deleteBuild(id: number) {
    return api.delete(`/systems/builds/${id}`);
}

export default {
    getEmulators,
    getEmulator,
    updateEmulator,
    deleteEmulator,
    getBuilds,
    getBuild,
    updateBuild,
    deleteBuild,
};
