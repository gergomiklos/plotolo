"use client";

import React from "react";
import {useCallback, useEffect, useRef, useState} from "react";
import cookies from 'js-cookie';
import debounce from 'lodash.debounce';
import {
  createRequestMessage, createScriptState,
  RequestMessage,
  ScriptState,
  Widget,
  WidgetData
} from "@/types";
import useDataStorage from "@/lib/useDataStorage";


const SESSION_COOKIE_NAME = 'PLOTOLO_SESSION_ID';

let websocket: WebSocket | null = null;


export default function useAppSession(appId: string) {
  const dataStorage = useDataStorage();

  useEffect(() => {
    dataStorage.setActiveAppId(appId);
  }, [appId]);

  const [widgets, setWidgets] = useState<Widget[]>([]);
  const [scriptState, setScriptState] = useState<ScriptState>(createScriptState());

  const connectWebsocket = async (auth = false) => {
    // Authenticates session if needed
    if (auth || !cookies.get(SESSION_COOKIE_NAME)) {
      await authenticateSession(appId);
    }

    if (!appId) {
      return;
    }

    if (websocket) {
      websocket.onclose = null;
      websocket.close();
    }
    websocket = new WebSocket(`ws:localhost:8088/apps/ws/${appId}`);
    websocket.onmessage = listenWebsocketMessages;
    websocket.onclose = listenWebsocketClose;
  }

  useEffect(() => {
    connectWebsocket();

    return () => {
      if (websocket) {
        websocket.onclose = null;
        websocket.close();
      }
    }
  }, [appId]);

  const updateWidgets = (widgets: Widget[]) => {
    setWidgets(widgets);
  }

  const updateDataStorage = (data: WidgetData) => {
    requestedDataRef.current = requestedDataRef.current.filter(hash => !data[hash]);
    dataStorage.updateData(data);
  }

  const updateScriptState = (scriptState: ScriptState) => {
    scriptState.errors.forEach(error => console.error('App error:', error));
    setScriptState(scriptState);
  }

  // Subscribes states to new events
  const listenWebsocketMessages = (event) => {
    const message = JSON.parse(event.data);

    message.widget_data && updateDataStorage(message.widget_data);
    message.widget_states && updateWidgets(message.widget_states);
    message.script_state && updateScriptState(message.script_state);
  }

  const listenWebsocketClose = ({code}) => {
    switch (code) {
      case 404:
        console.error('App not found');
        break;
      case 401:
        console.warn("Not authenticated");
        connectWebsocket(true);
        break;
      default:
        console.warn('Websocket connection was closed, trying to reconnect');
        setTimeout(() => connectWebsocket(), 1000);
    }
  }

  // Store pending requests to send them in batches with a debouncer
  const requestsRef = useRef<RequestMessage>(createRequestMessage());
  // Stores all the hashes for the already requested/pending data requests
  // to avoid requesting the same data multiple times
  const requestedDataRef = useRef<string[]>([]);

  // Debounced function to send requests to the backend in batches
  const sendRequests = useCallback(
    debounce(async () => {
      websocket?.send(JSON.stringify(requestsRef.current));
      // clear sent requests
      requestsRef.current = createRequestMessage();

    }, 150, {maxWait: 1000}),
    []
  );

  // Debounced function to send only data requests to the backend in batches
  // with smaller wait time because the human factor is involved in this case
  const sendOnlyDataRequests = useCallback(
    debounce(async () => {
      const request = createRequestMessage({data_requests: requestsRef.current.data_requests});
      requestsRef.current.data_requests = [];
      requestedDataRef.current = [];

      websocket?.send(JSON.stringify(request));
    }, 5, {maxWait: 50}),
    []
  );

  // Add input request to the pending requests for sending
  const addInputRequest = ({widget_id, data_update}: { widget_id: string, data_update: Record<string, any> }) => {
    requestsRef.current.input_requests[widget_id] = {
      ...(requestsRef.current.input_requests[widget_id] || {}),
      ...data_update
    };
    sendRequests();
  }

  // Add data request to the pending requests for sending if it's not already there
  const addDataRequest = (hash: string) => {
    if (!requestedDataRef.current.includes(hash)) {
      requestedDataRef.current.push(hash);
      if (!requestsRef.current.data_requests.includes(hash)) {
        requestsRef.current.data_requests.push(hash);
        sendOnlyDataRequests();
      }
    }
  }

  // Finds and requests missing data for all the widgets
  const requestMissingData = (widgets: Widget[]) => {
    widgets.forEach(widget => lookupWidgetData(widget.hash_state));
  }

  // Returns key2data pairs for key2hash pairs and creates data requests if missing
  const lookupWidgetData = (hash_state: Record<string, any> = {}) => {
    const widgetData = {};
    Object.entries(hash_state).forEach(([key, hash]) => {
      widgetData[key] = lookupData(hash);
    })
    return widgetData;
  }

  // Returns data for a hash with and creates a data request if missing
  // Returns data for a hash with and creates a data request if missing
  const lookupData = (hash: string) => {
    const data = dataStorage.getData(hash);

    if (data === undefined) {
      addDataRequest(hash);
    }
    return data;
  }

  // Listens for changes in the widgets and requests any missing data for them
  useEffect(() => {
    requestMissingData(widgets);
  }, [widgets]);

  return {widgets, scriptState, addInputRequest};
}


// Sends a request to the backend to authenticate the session
const authenticateSession = async (appId) => {
  await fetch(`/server/auth/${appId}`, {
    method: 'GET',
    credentials: 'include',
  });
}