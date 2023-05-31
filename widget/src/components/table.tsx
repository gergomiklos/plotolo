"use client"

import React from "react";
import {WidgetPropsType} from "./types";


export default function Table({data}: WidgetPropsType) {
  const tableData = data.data || [[]]
  const columns = data.columns || []

  //g:overflow-auto scrollbar:!w-1.5 scrollbar:!h-1.5 scrollbar:bg-transparent scrollbar-track:!bg-slate-100
  // scrollbar-thumb:!rounded scrollbar-thumb:!bg-slate-300 scrollbar-track:!rounded dark:scrollbar-track:!bg-slate-500/[0.16]
  // dark:scrollbar-thumb:!bg-slate-500/50 max-h-96 lg:supports-scrollbars:pr-2

  return (
    <div className="rounded-2xl ring ring-1 ring-gray-50 overflow-hidden shadow-md">

      <div className="overflow-auto max-w-4xl max-h-[80vh]">
        <table className="min-w-full border-separate border-spacing-0 scrollbar:bg-transparent ">
          <thead>
          <tr>
            {columns.map((column) => (
              <th
                key={column}
                scope="col"
                className="sticky top-0 border-b border-gray-300 bg-white bg-opacity-90 py-3.5 pl-4 pr-3 text-left
                text-sm font-semibold text-gray-900 sm:pl-6 lg:pl-8"
              >
                {column}
              </th>
            ))}
          </tr>
          </thead>
          <tbody className="bg-gray-50">
          {tableData.map((row, rowIdx) => (
            <tr key={rowIdx}>
              {row.map((cell, cellIdx) => (
                <td
                  key={cellIdx}
                  className={classNames(
                    'whitespace-nowrap py-4 pl-4 pr-3 text-sm text-gray-900 sm:pl-6 lg:pl-8'
                  )}
                >
                  {cell}
                </td>
              ))}
            </tr>
          ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

const classNames = (...classes) => classes.filter(Boolean).join(' ')

