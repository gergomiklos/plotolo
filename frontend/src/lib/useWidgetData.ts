import useDataStorage from "@/lib/useDataStorage";


export const useWidgetData = (key2hash: Record<string, string>) => {
  // Convert key2hash to key2data with data lookup
  return useDataStorage(state => {
    const key2data = {};
    Object.entries(key2hash).forEach(([key, hash]) => key2data[key] = state.data[hash]);
    return key2data;
  })
}