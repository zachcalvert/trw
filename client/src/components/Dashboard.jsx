import React, { useEffect, useState } from 'react';
import axios from "axios";

import { API_URL } from "../constants";
import { WorkOrder } from './WorkOrders/WorkOrder.jsx'


export const Dashboard = ()  => {
  const [workOrders, setWorkOrders] = useState([]);

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