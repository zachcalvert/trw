import React from 'react'
import { Typography } from '@material-ui/core';
import './Checkpoint.css';

export const Checkpoint = (props)  => {
  const { checkpoint } = props;
  const { percent_of_total } = checkpoint;

  return (
    <div className="checkpoint">
      <Typography style={{ height: percent_of_total }}variant='subtitle'>{ checkpoint.goal }</Typography>
    </div>
  )
};