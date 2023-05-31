import type {StoryObj} from '@storybook/react';
import '../src/index.css'
import {Table} from '../src/components';


// More on how to set up stories at: https://storybook.js.org/docs/react/writing-stories/introduction
const meta = {
  title: 'Widget/Table',
  component: Table,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
  }
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    id: 'id',
    data: {
      data: [
        ["data1", 300, 350, 300],
        ["data2", 130, 100, 140],
        ["data2", 130, 100, 140],
      ],
      columns: ["col1", "col2", "col3", "col4"],
    },
  },
};



