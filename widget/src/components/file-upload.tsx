"use client"

import React, {useRef, useState} from "react";
import {WidgetPropsType} from "./types";
import {ArrowUpTrayIcon} from "@heroicons/react/20/solid";
import {CheckCircleIcon} from "@heroicons/react/24/outline";


export default function FileUpload({id, data, on_input, embedded = false}: WidgetPropsType) {
  const label = data.label || ''
  const path = data.path || ''

  const [success, setSuccess] = useState(false)
  const [waiting, setWaiting] = useState(false)
  const successTimeoutRef = useRef<any>(null)

  const onUpload = async (event) => {
    const selectedFile = event.target.files ? event.target.files[0] : null

    if (embedded) {
      // todo fileserver doesn't run in inline mode
      on_input({widget_id: id, data_update: {uploaded_filename: selectedFile.name}})
      return
    }

    if (selectedFile)
      try {
        setWaiting(true)

        const formData = new FormData();
        formData.append('file', selectedFile, selectedFile.name);
        const response = await fetch(`/server/file/${path}`, {
          method: 'POST',
          body: formData,
          credentials: 'include',
        });

        setWaiting(false)

        if (response.ok) {
          setSuccess(true)
          successTimeoutRef.current = setTimeout(() => setSuccess(false), 5000)
          on_input({widget_id: id, data_update: {uploaded_filename: selectedFile.name}})
        } else {
          if (response.status === 0) {
            console.warn('Cors warning: could not read response from server.')
          } else if (response.status === 413) {
            alert('File is too large. Please select a file smaller one.');
          } else {
            alert('Error while uploading file.');
          }
        }
      } catch (e) {
        console.error(e)
        alert('Error while uploading file.');
        setWaiting(false)
      }
  };

  return (
    <>
      <label className={`relative block w-full max-w-sm px-3 py-2 rounded-xl border-2 border-dashed border-blue-100 
      text-center hover:border-blue-200 focus:outline-none focus:ring-2 focus:ring-blue-50 focus:ring-offset-2 
      bg-blue-50 text-blue-600 text-sm font-semibold flex justify-center items-center gap-x-2 
      ${waiting && 'bg-blue-50 border-blue-100 animate-pulse'}`}>
        <input
          disabled={waiting}
          type="file"
          onChange={onUpload}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />
        {success ? <CheckCircleIcon className="h-6 w-6"/> : <ArrowUpTrayIcon className="h-6 w-5"/>}
        {label}
      </label>
    </>
  )
};
