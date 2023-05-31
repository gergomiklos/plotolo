import type {StoryObj} from '@storybook/react';
import '../src/index.css'
import {Slider} from '../src/components';


const meta = {
  title: 'Widget/Slider',
  component: Slider,
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
      label: 'Choose a value:',
      min: 0,
      max: 100,
      default_value: 50,
    },
  },
};



