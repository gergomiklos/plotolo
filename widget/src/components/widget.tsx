"use client"

import React from "react";
import {WidgetPropsType} from "./types";
import {
  Button,
  Checkbox,
  Select,
  TextInput,
  Text,
  Title,
  Markdown,
  Slider,
  Table,
  Divider,
  FileUpload,
  FileDownload,
  Image,
  AreaChart,
} from "./";


export default function Widget(props: WidgetPropsType) {

  switch (props.type) {
    case 'TEXT':
      return <Text {...props} />
    case 'TEXT_INPUT':
      return <TextInput {...props} />
    case 'BUTTON':
      return <Button {...props} />
    case 'CHECKBOX':
      return <Checkbox {...props} />
    case 'SELECT':
      return <Select {...props} />
    case 'TITLE':
      return <Title {...props} />
    case 'MARKDOWN':
      return <Markdown {...props} />
    case 'SLIDER':
      return <Slider {...props} />
    case 'TABLE':
      return <Table {...props} />
    case 'DIVIDER':
      return <Divider {...props} />
    case 'FILE_UPLOAD':
      return <FileUpload {...props} />
    case 'FILE_DOWNLOAD':
      return <FileDownload {...props} />
    case 'IMAGE':
      return <Image {...props} />
    case 'AREA_CHART':
      return <AreaChart {...props} />
    default:
      console.warn('Unknown widget type: ' + props.type)
      return <div/>
  }
}
