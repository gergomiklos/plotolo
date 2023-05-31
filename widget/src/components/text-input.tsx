"use client"

import React, {useState} from "react";
import {WidgetPropsType} from "./types";
import {valueFallback} from "./utils";


export default function TextInput({id, data, on_input}: WidgetPropsType) {
  const label = data.label;
  const serverValue = data.value;
  const defaultValue = data.default_value || '';

  const [value, setValue] = useState(null);

  const actualValue = valueFallback(value, serverValue, defaultValue, '')

  const onChange = (value) => {
    setValue(value)
  }

  const onBlur = (value) => {
    setValue(value)
    if(value !== serverValue) {
      on_input({widget_id: id, data_update: {value}})
    }
  }

  return (
    <div className="w-full">
      <div className="text-gray-900">
        {label &&
          <div>
            {label}
          </div>
        }
        <input
          className="block mt-1 w-full max-w-sm rounded-xl border-0 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset
          ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-100 focus:outline-0"
          value={actualValue}
          onChange={e => onChange(e.target.value)}
          onBlur={event => onBlur(event.target.value)}
        />
      </div>
    </div>
  )
};
