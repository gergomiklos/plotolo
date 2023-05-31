import type {StoryObj} from '@storybook/react';
import '../src/index.css'
import {Markdown} from '../src/components';


const meta = {
  title: 'Widget/Markdown',
  component: Markdown,
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
      value:
`# Header :dog:
## Subheader :cat:
----
List:
- ($C_L$) is a dimensionless coefficient :+1:
- _italic_
- __bold__`,
    },
  },
};



