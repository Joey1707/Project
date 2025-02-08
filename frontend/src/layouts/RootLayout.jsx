import { Outlet } from "react-router";
import { useEffect } from "react";

// Google OAuth
import { gapi } from "gapi-script";
import { clientId } from "../utils/network_data";

// components
import Header from "../components/Header";

export default function RootLayout() {
	useEffect(() => {
		function start() {
			gapi.client.init({
				clientId: clientId,
				scope: "",
			});
		}

		gapi.load("client:auth2", start);
	}, []);

	return (
		<div className="flex flex-col h-screen">
			<Header />
			<main className="flex flex-col justify-center items-center h-full md:p-6 p-2 bg-gray-900">
				<Outlet />
			</main>
		</div>
	);
}
