import type {StoryObj} from '@storybook/react';
import '../src/index.css'
import {Title} from '../src/components';


const meta = {
  title: 'Widget/Title',
  component: Title,
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
      value: 'Title',
      size: 4,
    },
  },
};



