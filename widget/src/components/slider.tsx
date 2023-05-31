"use client"

import React, {useState} from "react";
import {WidgetPropsType} from "./types";
import {valueFallback} from "./utils";

export default function Slider({id, data, on_input}: WidgetPropsType) {
  const label = data.label;
  const serverValue = data.value;
  const defaultValue = data.default_value || '';
  const min = data.min || 0;
  const max = data.max || 100;

  const [value, setValue] = useState(null);
  const actualValue = valueFallback(value, serverValue, defaultValue, 0)

  const onChange = (value) => {
    setValue(value)
  }

  const onBlur = (value) => {
    setValue(value)
    if (value !== serverValue) {
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
        <div className="w-full max-w-sm flex items-center gap-x-2">
          <input
            type="range"
            min={min}
            max={max}
            value={actualValue}
            onChange={(e) => onChange(e.target.value)}
            //@ts-ignore
            onMouseUp={(e) => onBlur(e.target.value)}
            className="appearance-none bg-gray-300 rounded-full w-full h-1 "
          />
          <p className="text-gray-900">{actualValue}</p>
        </div>
      </div>
    </div>
  )
};
