import type {StoryObj} from '@storybook/react';
import '../src/index.css'
import {Text} from '../src/components';


const meta = {
  title: 'Widget/Text',
  component: Text,
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
      value: 'something',
    },
  },
};



