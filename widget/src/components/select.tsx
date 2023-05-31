"use client"

import React, {useState} from 'react'
import {WidgetPropsType} from "./types";
import {valueFallback} from "./utils";

export default function Select({id, data, on_input}: WidgetPropsType) {
  const label = data.label || ''
  const options = data.options || []
  const defaultValue = data.default_value || options.at(0) || ''
  const serverValue = data.value || ''

  const [value, setValue] = useState(null)
  const actualValue = valueFallback(value, serverValue, defaultValue, '')

  const onChange = (value) => {
    setValue(value)
    on_input({widget_id: id, data_update: {value}})
  }

  return (
    <div className="w-full">
      {label &&
        <label className="text-gray-900">
          {label}
        </label>
      }
      <select
        className="mt-1 max-w-sm block w-full rounded-xl border-0 py-1.5 pl-3 pr-10 text-gray-900 shadow-sm ring-1 ring-inset
          ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-100 focus:outline-0"
        onChange={e => onChange(e.target.value)}
        value={actualValue}
      >
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </div>
  )
};
