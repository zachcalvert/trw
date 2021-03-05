import React, { useEffect, useState } from 'react';

import axios from "axios";
import { API_URL } from "../constants";


export const Dashboard = ()  => {
  const [workOrders, setWorkOrders] = useState([]);

  useEffect(() => {
    async function fetchWorkOrders() {
      const { data } = await axios.get(API_URL);
      console.log(data);
      setWorkOrders(data);
    }
    fetchWorkOrders();
  }, []);

  return (
    <>
      {workOrders.map(workorder => (
        <div key={workorder.name} className={`workorder workorder-${workorder.name}`}>
          {workorder.name}
        </div>
      ))}
    </>
  )
};