import type {StoryObj} from '@storybook/react';
import '../src/index.css'
import {TextInput} from '../src/components';


const meta = {
  title: 'Widget/TextInput',
  component: TextInput,
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
      label: 'Write something:',
      default_value: 'something',
    },
  },
};



