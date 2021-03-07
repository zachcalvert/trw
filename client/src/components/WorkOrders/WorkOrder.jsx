import React from 'react';
import { LinearProgress, Typography } from '@material-ui/core';

import { Checkpoint } from '../Checkpoints/Checkpoint.jsx'

import './WorkOrder.css';

export const WorkOrder = (props)  => {
  const { workOrder } = props;
  const height = (workOrder.published / workOrder.goal) * 100;
  const integrity = workOrder.published > workOrder.ideal_published;

  return (
    <div className="workorder">
    
      {workOrder.checkpoints.map((checkpoint, index) => {
        <div key={index}>
          <Checkpoint checkpoint={checkpoint} />
        </div>
      })}

      <LinearProgress className={integrity ? 'blue-progress' : 'red-progress'}  variant="determinate" value={height} />
      
      <div className={integrity ? 'blue-bubble' : 'red-bubble'}>
        <div className='bubble-text-wrapper'>
          <div className='valign'>
            <Typography variant='h6'>{workOrder.name}</Typography>
          </div>
        </div>
      </div>
    
    </div>
  )
};