import {create, StateCreator} from "zustand";
import {persist} from 'zustand/middleware'
import {App} from "@/types";


export interface Storage {
  data: Record<string, any>;
  updateData: (data_update: Record<string, any>) => void;
  getData: (hash: string) => Record<string, any>;

  activeAppId: string | null;
  setActiveAppId: (appId: string) => void;

  apps: App[];
  fetchApps: () => void;
}


export const createDataStorage: StateCreator<Storage> = (set, get) => ({
  // widget data
  data: {},
  updateData: (data_update) => {
    set((state) => ({data: {...state.data, ...data_update}}));
  },
  getData: (hash: string) => {
    return get().data[hash];
  },

  // app
  activeAppId: null,
  setActiveAppId: (appId) => {
    if (appId && get().activeAppId && get().activeAppId !== appId) {
      // clear data cache if app changed
      set({data: {}});
    }
    set({activeAppId: appId});
  },

  // apps
  apps: [],
  fetchApps: async () => {
    const response = await fetch('/server/apps');
    const apps = (await response.json()) || [];
    set({apps});
  }
})


const useDataStorage = create<Storage>()(
  persist(
    (...a) => ({
      ...createDataStorage(...a),
    }),
    {name: 'PLOTOLO-DATA-STORAGE'}
  )
)

export default useDataStorage;