import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Orders = () => {
    const [orders, setOrders] = useState([]);

    useEffect(() => {
        const fetchOrders = async () => {
            try {
                const token = localStorage.getItem("access_token");  // Asegúrate de que el token esté almacenado
                const response = await axios.get('http://localhost:5000/api/orders', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                setOrders(response.data);
            } catch (error) {
                console.error("Error fetching orders", error);
            }
        };

        fetchOrders();
    }, []);

    return (
        <div>
            <h1>Orders</h1>
            <ul>
                {orders.map(order => (
                    <li key={order.id}>
                        Order Number: {order.number} - Total: {order.total}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Orders;