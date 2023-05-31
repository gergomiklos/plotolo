
export type onInputType = ({widget_id, data_update}: { widget_id: string, data_update: Record<string, any> }) => void;

export type WidgetPropsType = { id: string, status: string, type: string, data: Record<string, any>, on_input: onInputType, embedded: boolean }