import type {StoryObj} from '@storybook/react';
import '../src/index.css'
import {FileUpload} from '../src/components';


// More on how to set up stories at: https://storybook.js.org/docs/react/writing-stories/introduction
const meta = {
  title: 'Widget/FileUpload',
  component: FileUpload,
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
      label: 'Upload',
      path: '#',
    },
  },
};



