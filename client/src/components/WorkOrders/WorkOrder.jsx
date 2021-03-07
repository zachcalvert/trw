import React from 'react';
import { Paper, Typography } from '@material-ui/core';

import { Checkpoint } from '../Checkpoints/Checkpoint.jsx'

import './WorkOrder.css';

export const WorkOrder = (props)  => {
  const { workOrder } = props;
  const height = (workOrder.published / workOrder.goal) * 100;
  const integrity = workOrder.published > workOrder.ideal_published;

  console.log({workOrder})

  return (
    <Paper className="workorder">

      {workOrder.checkpoints.map(checkpoint => (
        <Checkpoint checkpoint={checkpoint} />
      ))}
    
      <div className={integrity ? 'vertical-progress' : 'vertical-progress red'}></div>
      
      <div className={integrity ? 'blue bubble' : 'red bubble'}>
        <div className='bubble-text-wrapper'>
          <div className='valign'>
            <Typography variant='h6'>{workOrder.name}</Typography>
          </div>
        </div>
      </div>
    
    </Paper>
  )
};