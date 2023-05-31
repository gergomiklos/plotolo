"use client"

import React from "react";
import {Widget as WidgetType} from "@/types";
import {useWidgetData} from "@/lib/useWidgetData";
import {Widget, onInputType} from "plotolo-widget"


type WebWidgetPropsType = {
  widget: WidgetType,
  onInput: onInputType,
  scriptStatus: string,
}


export default function WebWidget({widget, onInput, scriptStatus}: WebWidgetPropsType) {
  const {id, type, status} = widget;
  const data = useWidgetData(widget.hash_state);
  const props = {id, status, type, embedded: false, data, on_input: onInput};

  const isWaiting = (status === "PENDING" && scriptStatus == "RUNNING");

  return (
    <div className={`${isWaiting ? 'opacity-60' : ''}`}>
      <Widget {...props} />
    </div>
  )
}
