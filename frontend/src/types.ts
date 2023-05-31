
export type App = {
  id: string,
  name: string,
}

export function createApp({id = "", name = ""}: Partial<App> = {}) {
  return {
    id,
    name,
  } as App
}


export type ResponseMessage = {
  widget_states: Widget[],
  widget_data: WidgetData[],
  script_state: ScriptState,
}

export function createResponseMessage({
                                        widget_states = [],
                                        widget_data = [],
                                        script_state = createScriptState()
                                      }: Partial<ResponseMessage> = {}) {
  return {
    widget_states,
    widget_data,
    script_state,
  } as ResponseMessage
}


export type Widget = {
  id: string,
  status: string,
  type: string,
  hash_state: Record<string, any>
}

export function createWidget({id = "", status = "", type = "", hash_state = {}}: Partial<Widget> = {}) {
  return {
    id,
    status,
    type,
    hash_state,
  } as Widget
}


export type WidgetData = Record<string, any>

export function createWidgetData(data: WidgetData = {}) {
  return data as WidgetData
}


export type ScriptState = {
  status: string,
  errors: string[],
}

export function createScriptState({status = "STOPPED", errors = []}: Partial<ScriptState> = {}) {
  return {
    status,
    errors,
  } as ScriptState;
}


export type RequestMessage = {
  data_requests: string[],
  input_requests: Record<string, Record<string, any>>,
}

export function createRequestMessage({data_requests = [], input_requests = {}}: Partial<RequestMessage> = {}) {
  return {
    data_requests,
    input_requests,
  } as RequestMessage
}