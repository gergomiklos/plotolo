'use client'

import React, {useEffect, useRef} from 'react';
import bb, {area, areaSpline, subchart, zoom} from 'billboard.js';
import {WidgetPropsType} from "./types";


const LineChart = ({data}: WidgetPropsType) => {
  const chartData = data.data || [[]]
  const isSpline = data.spline || false
  const isZoom = data.zoom || false
  const isSubchart = data.subchart || false
  const isLegend = data.legend || true
  const isTooltip = data.tooltip || true
  const isLinearGradient = data.linear_gradient || true

  const chartContainer = useRef(null);
  let chart = null;

  useEffect(() => {
    if (!chart) {
      chart = bb.generate({
        data: {
          columns: chartData,
          type: isSpline ? areaSpline() : area(),
        },
        zoom: {
          enabled: isZoom ? zoom() : false,
          type: "drag"
        },
        area: {
          linearGradient: isLinearGradient,
        },
        subchart: {
          show: isSubchart ? subchart() : false,
          showHandle: false
        },
        legend: {
          show: isLegend
        },
        tooltip: {
          show: isTooltip
        },
        bindto: chartContainer.current
      });
    } else {
      chart.load({
        columns: chartData
      });
    }
  }, [data]);

  return (
    <>
      <div ref={chartContainer}></div>
    </>
  );
};

export default LineChart;

