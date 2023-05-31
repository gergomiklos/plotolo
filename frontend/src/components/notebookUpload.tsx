import React, {useState} from "react";
import {CheckCircleIcon} from "@heroicons/react/24/outline";
import {ArrowUpTrayIcon} from "@heroicons/react/20/solid";


export default function NotebookUpload() {
  const [success, setSuccess] = useState(false)
  const [waiting, setWaiting] = useState(false)

  const onUpload = async (event) => { // todo refetch, maybe through store

    const selectedFile = event.target.files ? event.target.files[0] : null;
    if (selectedFile)
      try {
        setWaiting(true)

        const formData = new FormData();
        formData.append('file', selectedFile, selectedFile.name);
        const response = await fetch(`/server/scripts`, {
          method: 'POST',
          body: formData,
          credentials: 'include',
        });

        setWaiting(false);

        if (response.ok) {
          setSuccess(true);
          setTimeout(() => setSuccess(false), 5000);
        } else {
          if (response.status === 0) {
            console.warn('Cors warning: could not read response from server.');
          } else if (response.status === 413) {
            alert('File is too large. Please select a file smaller one.');
          } else if (response.status === 400) {
            alert('Error: ' + (await response.text()));
          } else {
            alert('Error while uploading file.');
          }
        }
      } catch (e) {
        console.error(e);
        alert('Error while uploading file.');
        setWaiting(false);
      }
  };

  return (
    <div className="p-5 w-full">
      <label className={`relative block w-full px-3 py-2 rounded-xl border-2 border-dashed border-blue-100 
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
        Upload New Notebook
      </label>
    </div>
  )
}
