import React, { useState, useEffect } from 'react'
import { useTransition, animated } from 'react-spring'
import { LinearProgress, Typography } from '@material-ui/core';

import './WorkOrder.css';

export const WorkOrder = (props)  => {
  const { workOrder } = props;
  const height = (workOrder.published / workOrder.goal) * 100;
  const integrity = workOrder.published > workOrder.ideal_published;
  const [index, set] = useState(0)
  const transitions = useTransition(index, p => p, {
    from: { opacity: 0, transform: 'translate3d(100%,0,0)' },
    enter: { opacity: 1, transform: 'translate3d(0%,0,0)' },
    leave: { opacity: 0, transform: 'translate3d(-50%,0,0)' },
  })

  const pages = [
    ({ style }) => <animated.div style={{ ...style }}>{workOrder.name}</animated.div>,
    ({ style }) => <animated.div style={{ ...style }}>Published target {workOrder.ideal_published}</animated.div>,
    ({ style }) => <animated.div style={{ ...style }}>Published actual {workOrder.published}</animated.div>,
  ]

  useEffect(() => void setInterval(() => set(state => (state + 1) % 3), 3000), [])

  return (
    <div className="workorder">
      <LinearProgress className={integrity ? 'green-progress' : 'red-progress'}  variant="determinate" value={height} />
      <div className={integrity ? 'blue-bubble' : 'red-bubble'}>
        <div className='bubble-text-wrapper'>
          <div className='valign'>
            <div className="simple-trans-main">
              {transitions.map(({ item, props, key }) => {
                const Page = pages[item]
                return <Page key={key} style={props} />
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
};