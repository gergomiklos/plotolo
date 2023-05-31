"use client"

import React from "react";
import {WidgetPropsType} from "./types";

export default function Text({data}: WidgetPropsType) {

  return (
    <>
      <div className="text-gray-900">
        {data.value || ''}
      </div>
    </>
  )
};
