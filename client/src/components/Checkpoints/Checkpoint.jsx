import React from 'react'
import { Typography } from '@material-ui/core';
import './Checkpoint.css';

export const Checkpoint = (props)  => {
  const { checkpoint } = props;
  const { percent_of_total } = checkpoint;
  const { short_date } = checkpoint;

  return (
    <div className="checkpoint" style={{ top: `calc(100% - ${percent_of_total}%)` }}>
      <Typography variant='overline' style={{ height: percent_of_total }}variant='subtitle'>
        { short_date }&nbsp;&nbsp;----&nbsp;&nbsp;{ checkpoint.goal }
      </Typography>
    </div>
  )
};