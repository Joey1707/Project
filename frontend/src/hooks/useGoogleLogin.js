import { useEffect, useState } from "react";
import { jwtDecode } from "jwt-decode";
import { clientId, putAccessToken } from "../utils/network_data";
import { useNavigate } from "react-router";

function useGoogleLogin() {
	const [user, setUser] = useState({});
	const navigate = useNavigate();

	function handleCallbackResponse(response) {
		console.log("encoded JWT ID token: ", response.credential);
		const token = response.credential;
		const decoded = jwtDecode(token);
		console.log(decoded);
		setUser(decoded);

		putAccessToken(decoded.jtw);
		navigate("/dashboard");
	}

	function handleSignOut(event) {
		// Sign out from Google
		google.accounts.id.revoke(user?.sub, () => {
			console.log("User signed out from Google");
			setUser({}); // Clear the user state in your app
		});
	}

	useEffect(() => {
		google.accounts.id.initialize({
			client_id: clientId,
			callback: handleCallbackResponse,
		});
		google.accounts.id.renderButton(document.getElementById("signInDiv"), {
			theme: "outline",
			size: "Large",
		});
	}, []);

	return [user, handleSignOut];
}

export default useGoogleLogin;
