"use client"

import React from "react";
import {WidgetPropsType} from "./types";

export default function Image({data}: WidgetPropsType) {
  const base64 = data.base64 || '';
  const type = data.type || '';

  return (
    <>
      <img src={`data:image/${type};base64,${base64}`} alt="image" className="rounded-xl"/>
    </>
  )
};
