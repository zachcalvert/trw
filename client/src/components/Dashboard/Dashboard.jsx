import React, { useEffect, useState } from 'react';
import axios from "axios";
import { makeStyles } from '@material-ui/core/styles';
import { Grid, Paper } from '@material-ui/core';

import { API_URL } from "../../constants";
import { WorkOrder } from '../WorkOrders/WorkOrder.jsx'

import './Dashboard.css';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  paper: {
    height: '100%',
    width: 200,
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
    <Grid container className={classes.root} spacing={2}>
      <Grid item xs={12}>
        <Grid container justify="center" spacing={5}>
          {workOrders.map(workOrder => (
            <Grid key={workOrder.name} item>
              <Paper className={classes.paper}>
                <WorkOrder workOrder={workOrder} />
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Grid>
    </Grid>
  )
};