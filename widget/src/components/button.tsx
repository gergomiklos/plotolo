"use client"

import React from "react";
import {WidgetPropsType} from "./types";

export default function Button({id, data, on_input}: WidgetPropsType) {
  const label = data.label || ''
  const clicked = data.clicked || false

  const onClick = () => {
    on_input({widget_id: id, data_update: {clicked: true}})
  }

  return (
    <>
      <button
        disabled={clicked}
        className="rounded-xl bg-blue-50 px-3 py-2 text-sm font-semibold text-blue-600 shadow-sm hover:bg-blue-100
        disabled:bg-blue-50"
        onClick={onClick} type="button">
        {label}
      </button>
    </>
  )
};
