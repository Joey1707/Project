import {
	createBrowserRouter,
	createRoutesFromElements,
	Route,
	RouterProvider,
} from "react-router";
import { useMemo, useState } from "react";
import { clientId } from "./utils/network_data";

// Contexts
import UserContext from "./contexts/UserContext";
import { GoogleOAuthProvider } from "@react-oauth/google";

// pages
import LoginPage from "./pages/LoginPage";
import HomePage from "./pages/HomePage";
import NotFoundPage from "./pages/NotFoundPage";
import DashboardPage, { dashboardLoader } from "./pages/DashboardPage";
import DataInputPage, { dataInputLoader } from "./pages/DataInputPage";
import RegisterPage from "./pages/RegisterPage";
import ErrorPage from "./pages/ErrorPage";

// layouts
import RootLayout from "./layouts/RootLayout";

const router = createBrowserRouter(
	createRoutesFromElements(
		<Route path="/" element={<RootLayout />}>
			<Route index element={<HomePage />} />
			<Route path="dashboard" element={<DashboardPage />} loader={dashboardLoader} errorElement={<ErrorPage/>}/>
			<Route path="input" element={<DataInputPage />} loader={dataInputLoader} errorElement={<ErrorPage/>}/>

			<Route path="register" element={<RegisterPage />} />
			<Route path="login" element={<LoginPage />} />

			<Route path="*" element={<NotFoundPage />} />
		</Route>
	)
);

function App() {
	const [userInfo, setUserInfo] = useState(null);

	const userInfoValue = useMemo(() => {
		return {
			userInfo,
			setUserInfo,
		};
	}, [userInfo]);

	return (
		<GoogleOAuthProvider clientId={clientId}>
			<UserContext.Provider value={userInfoValue}>
				<RouterProvider router={router} />
			</UserContext.Provider>
		</GoogleOAuthProvider>
	);
}

export default App;
