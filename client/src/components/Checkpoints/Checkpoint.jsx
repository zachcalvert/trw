import React from 'react'
import { Typography } from '@material-ui/core';
import './Checkpoint.css';

export const Checkpoint = (props)  => {
  const { checkpoint } = props;
  const { percent_of_total } = checkpoint;
  const { short_date } = checkpoint;

  return (
    <>
      <div className="checkpoint date" style={{ top: `calc(100% - ${percent_of_total}%)` }}>
        <Typography variant='subtitle1'>
          { short_date }
        </Typography>
      </div>
      <div className="checkpoint goal" style={{ top: `calc(100% - ${percent_of_total}%)` }}>
        <Typography variant='subtitle1'>
          { checkpoint.goal }
        </Typography>
      </div>
    </>
  )
};