"use client"

import React from "react";
import {WidgetPropsType} from "./types";

export default function Title({data}: WidgetPropsType) {
  const level = data.level || 3;

  const fontSize = {
    1: 'text-lg',
    2: 'text-xl',
    3: 'text-2xl',
    4: 'text-3xl',
    5: 'text-4xl',
  }[level];

  return (
    <>
      <div className="hidden text-lg text-xl text-2xl text-3xl text-4xl"></div>
      <div className={`${fontSize} font-bold text-gray-900`}>
        {data.value || ''}
      </div>
    </>
  )
};
