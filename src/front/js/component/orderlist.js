import React, { useContext } from "react";
import { Context } from "../store/appContext";
import "../../styles/home.css";
import OrderList from "../component/orderlist";

export const Home = () => {
    const { store, actions } = useContext(Context);

    return (
        <div className="text-center mt-5">
            <h1>Pedidos</h1>
            <OrderList />
        </div>
    );
};
const OrderList = () => {
    const { store, actions } = useContext(Context); // Obtener el store y las acciones

    useEffect(() => {
        actions.getOrders(); // Llamar a la acción para obtener órdenes al montar el componente
    }, []);

    return (
        <div>
            <h1>Order List</h1>
            <ul>
                {store.orders.length > 0 ? ( // Acceder a las órdenes desde el store
                    store.orders.map(order => (
                        <li key={order.id}>
                            <h2>Order #{order.number}</h2>
                            <p>Status: {order.status}</p>
                            <p>Created via: {order.created_via}</p>
                            <p>Order Key: {order.order_key}</p>
                            {/* Agrega más detalles si es necesario */}
                        </li>
                    ))
                ) : (
                    <p>No orders available.</p>
                )}
            </ul>
        </div>
    );
};

export default OrderList;
