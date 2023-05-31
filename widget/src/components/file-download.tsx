"use client"

import React from "react";
import {WidgetPropsType} from "./types";
import {ArrowDownTrayIcon} from "@heroicons/react/20/solid";


// todo fileserver doesn't run in inline mode
export default function FileDownload({id, data, on_input, embedded = false}: WidgetPropsType) {
  const label = data.label || ''
  const filepath = data.filepath || ''

  const isRelativePath = !filepath.startsWith('http')
  const realPath = (isRelativePath ? (embedded ? '#' : `api/file/${filepath}`) : filepath)
  const filename = filepath.split('/').pop();

  const onClick = () => {
    on_input({widget_id: id, data_update: {downloaded: true}})
  }

  return (
    <>
      <a
        download={filename} href={realPath} onClick={onClick}
        className="block w-fit rounded-xl bg-blue-50 px-3 py-2 text-sm font-semibold text-blue-600 shadow-sm hover:bg-blue-100
        disabled:bg-blue-50 flex items-center justify-center gap-x-2"
      >
        <ArrowDownTrayIcon className="h-5 w-5"/>
        {label}
      </a>
    </>
  )
};
