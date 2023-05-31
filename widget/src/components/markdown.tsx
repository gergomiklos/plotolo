"use client"

import React from "react";
import {WidgetPropsType} from "./types";
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import remarkEmoji from 'remark-emoji'
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'

export default function Markdown({data}: WidgetPropsType) {

  return (
    <>
      <div className="markdown-body w-full">
        <ReactMarkdown
          remarkPlugins={[remarkGfm, remarkEmoji, remarkMath]}
          rehypePlugins={[rehypeKatex]}>{data.value || ''}
        </ReactMarkdown>
      </div>
    </>
  )
};
