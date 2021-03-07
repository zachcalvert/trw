import React, { useEffect, useState } from 'react';
import axios from "axios";
import { makeStyles } from '@material-ui/core/styles';
import { API_URL } from "../../constants";
import { WorkOrder } from '../WorkOrders/WorkOrder.jsx'

import './Dashboard.css';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  paper: {
    height: '100%',
    width: '100%',
  },
  control: {
    padding: theme.spacing(2),
  },
}));

export const Dashboard = ()  => {
  const [workOrders, setWorkOrders] = useState([]);
  const classes = useStyles();

  useEffect(() => {
    async function fetchWorkOrders() {
      const { data } = await axios.get(API_URL);
      setWorkOrders(data);
    }
    fetchWorkOrders();
  }, []);

  return (
    <>
      {workOrders.map(workOrder => (
        <WorkOrder workOrder={workOrder} />
      ))}
    </>
  )
};