import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";
import "../../styles/navbar.css";

export const Navbar = () => {

	const navigate = useNavigate()

	const { store, actions } = useContext(Context);
	function handleLogout() {
		actions.logout()
		navigate('/')

	}

	return (
		<nav className="navbar  border-bottom border-body justify-content-between d-flex mb-5" id="navbar">
			<div className="container navbar">

				<div className="left-section">
					<h2 className="m-3">Wocoomerce Product Manager</h2>
					<h5 className="m-3">Gestión de fabricación y envío de productos de Woocommerce</h5>

				</div>

				<div className="links-section">
					<Link to="/demo">
						{store.auth === true ? <button className="btn " id="button" onClick={() => handleLogout()}>Pedidos</button> : ''}
					</Link>
					<Link to="/demo">
						{store.auth === true ? <button className="btn" id="button" onClick={() => handleLogout()}>Facturas</button> : ''}
					</Link>
					<Link to="/demo">
						{store.auth === true ? <button className="btn" id="button" onClick={() => handleLogout()}>Cambiar estados</button> : ''}

					</Link>

				</div>

				<div className="ml-auto">


					<div>
						{store.auth === true ? <button className="btn" onClick={() => handleLogout()}>Logout</button> : ''}
					</div>


				</div>
			</div>
		</nav>
	);
};
