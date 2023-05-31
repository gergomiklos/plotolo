"use client"

import React, {useState} from "react";
import {WidgetPropsType} from "./types";
import {valueFallback} from "./utils";

export default function Checkbox({id, data, on_input}: WidgetPropsType) {
  const label = data.label || ''
  const defaultValue = data.default_value || false
  const serverValue = data.value || false

  const [value, setValue] = useState(null)
  const actualValue = valueFallback(value, serverValue, defaultValue, false)

  const onChange = (value) => {
    setValue(value)
    on_input({widget_id: id, data_update: {value}})
  }

  return (
    <div className="w-full">
      <input
        type="checkbox"
        defaultChecked={defaultValue}
        value={actualValue}
        onChange={e => onChange(e.target.checked)}
        className="h-4 w-4 mr-2 mb-1 rounded-xl border-gray-300 text-blue-600 shadow-sm ring-1
          ring-gray-300 focus:ring-2 focus:ring-blue-100 focus:outline-0 "
      />
      {label &&
        <label className="text-gray-900">
          {label}
        </label>
      }
    </div>
  )
};
