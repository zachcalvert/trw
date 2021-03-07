import React from 'react'
import { Typography } from '@material-ui/core';
import './Checkpoint.css';

export const Checkpoint = (props)  => {
  const { checkpoint } = props;

  return (
    <div className="checkpoint">
      <Typography variant='subtitle'>{ checkpoint.goal }</Typography>
    </div>
  )
};