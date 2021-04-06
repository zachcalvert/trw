import React from 'react';
import { Paper, Typography } from '@material-ui/core';
import { Checkpoint } from '../Checkpoints/Checkpoint.jsx'

import './WorkOrder.css';

export const WorkOrder = (props)  => {
  const { workOrder } = props;
  const height = (workOrder.stocked / workOrder.goal) * 100;
  const integrity = workOrder.stocked >= workOrder.ideal_stocked;
  const todayStatus = workOrder.stocked - workOrder.ideal_stocked;
  const empty = workOrder.stocked === 0;

  return (
    <Paper className="workorder">
    
      <div className={integrity ? 'vertical-track light-green' : 'vertical-track light-red'}>
        <div className={integrity ? 'vertical-progress green' : 'vertical-progress red'} style={{ height: `${height}%` }}>
          <div className={integrity ? 'today-status ahead' : 'today-status behind'} style={{ bottom: `${height}%)` }}>
            <Typography variant='h6'>{integrity && '+'}{todayStatus}</Typography>
          </div>
        </div>

        {workOrder.checkpoints.map(checkpoint => (
          <Checkpoint checkpoint={checkpoint} />
        ))}
      </div>
      
      <div className={integrity ? empty ? 'bubble light-green' : 'bubble green' : empty ? 'bubble light-red' : 'bubble red'}>
        <div className='valign'>
          <Typography variant='h4'>{workOrder.name}</Typography>
        </div>
      </div>

      <div className='workorder-summary'>
        <Typography variant='subtitle1'>Stocked: {workOrder.stocked}</Typography>
        <Typography variant='subtitle1'>Published: {workOrder.published}</Typography>
        <Typography variant='subtitle1'>QA'd: {workOrder.qad}</Typography>
      </div>
    
    </Paper>
  )
};