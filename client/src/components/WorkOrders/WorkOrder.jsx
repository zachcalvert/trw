import React from 'react';
import { Paper, Typography } from '@material-ui/core';

import { Checkpoint } from '../Checkpoints/Checkpoint.jsx'

import './WorkOrder.css';

export const WorkOrder = (props)  => {
  const { workOrder } = props;
  const integrity = workOrder.published > workOrder.ideal_published;

  return (
    <Paper className="workorder">

      {workOrder.checkpoints.map(checkpoint => (
        <Checkpoint checkpoint={checkpoint} />
      ))}
    
      <div className={integrity ? 'vertical-track light-blue' : 'vertical-track light-red'} />
      {/* <div className={integrity ? 'vertical-progress blue' : 'vertical-progress red'}
           style={{ height: `${height}%` }}
       /> */}
      
      <div className={integrity ? 'bubble blue' : 'bubble red'}>
        <div className='valign'>
          <Typography variant='h6'>{workOrder.name}</Typography>
        </div>
      </div>
    
    </Paper>
  )
};