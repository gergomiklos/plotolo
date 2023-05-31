import type {StoryObj} from '@storybook/react';
import '../src/index.css'
import {Divider} from '../src/components';


const meta = {
  title: 'Widget/Divider',
  component: Divider,
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
  },
};



