import type {StoryObj} from '@storybook/react';
import '../src/index.css'
import '../src/billboard.min.css'
import {AreaChart} from '../src/components';


// More on how to set up stories at: https://storybook.js.org/docs/react/writing-stories/introduction
const meta = {
  title: 'Widget/AreChart',
  component: AreaChart,
  tags: ['autodocs'],
  parameters: {
    layout: 'fullscreen',
  }
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    id: 'id',
    data: {
      data: [
        ["data1", 300, 350, 300, 0, 0, 0],
        ["data2", 130, 100, 140, 200, 150, 50]
      ],
      subchart: true,
      zoom: true,
      linear_gradient: true,
      legend: true,
      tooltip: true,
      spline: true,
    },
  },
};



