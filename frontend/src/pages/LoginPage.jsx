// Hooks
import useGoogleLogin from "../hooks/useGoogleLogin.js";
import { useContext, useEffect } from "react";

// Components
import { NavLink, useNavigation } from "react-router";
import LoginForm from "../components/LoginForm";
import LoginGoogle from "../components/GoogleLoginButton.jsx";

// Context
import UserContext from "../contexts/UserContext.js";
import LoadingPage from "./LoadingPage.jsx";

export default function LoginPage() {
	const navigation = useNavigation()
	const [user] = useGoogleLogin();
	const { setUserInfo } = useContext(UserContext);

	useEffect(() => {
		setUserInfo(user);
	}, [user]);

	if (navigation.state === "loading") {
		return <LoadingPage/>
	}

	return (
		<section className="flex flex-row md:gap-6 gap-3 md:px-12 md:py-8 md:h-full h-80% lg:w-[60%] md:w-[70%] w-full">
			<div className="flex flex-col md:gap-3 gap-1 items-center justify-between bg-white rounded-md w-full p-6 shadow-xl">
				<h1 className="font-bold md:text-3xl text-xl border-b-2 border-dashed p-6 w-full text-center">
					Masuk ke akun anda
				</h1>
				<LoginForm />
				<p className="text-gray-600 font-medium border-t-2 p-6 w-full border-dashed text-center">
					Belum punya akun?{" "}
					<NavLink
						to="/register"
						className="text-blue-600 hover:underline"
					>
						Daftar akun
					</NavLink>
				</p>
				<LoginGoogle />
			</div>
		</section>
	);
}
