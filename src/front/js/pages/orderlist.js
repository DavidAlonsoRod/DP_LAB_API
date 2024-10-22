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