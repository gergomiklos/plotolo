import type {StoryObj} from '@storybook/react';
import '../src/index.css'
import {Select} from '../src/components';


const meta = {
  title: 'Widget/Select',
  component: Select,
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
      label: 'Choose a fruit:',
      options: ["apple", "pie", "cherry"],
      default_value: 'cherry',
    },
  },
};



