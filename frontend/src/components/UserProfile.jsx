// Hooks
import { useNavigate } from "react-router";
import { useContext } from "react";

// Components
import profilePlaceholder from "../assets/profile-placeholder.png";

// Utils
import { buttonHover } from "../styles/reusableSyles";

// Context
import UserContext from "../contexts/UserContext";

export default function UserProfile() {
	const navigate = useNavigate();
	const { userInfo, setUserInfo } = useContext(UserContext);

	const onLogoutHandler = () => {
		localStorage.removeItem("token");
		setUserInfo(null)
		navigate("/");
	};

	return (
		<div className="flex flex-col items-center h-full w-[20%] bg-white p-6 rounded-xl shadow-xl gap-6">
			<img
				src={profilePlaceholder}
				alt="profilePlaceholder"
				className="rounded-full bg-white w-full p-2 aspect-square border-2 border-gray-400"
			/>
			<div className="flex flex-col justify-between items-center h-full p-2 border-y-2">
				<div className="flex flex-col items-center justify-center gap-2">
					<h1 className="font-bold text-2xl">
						Welcome, {userInfo ? userInfo.username : "User"}!
					</h1>
					<p>
						Account email: {userInfo ? userInfo.email : "example@gmail.com"}
					</p>
				</div>
				<button
					onClick={onLogoutHandler}
					className={
						"font-bold border-4 rounded-md text-xl p-2 w-full cursor-pointer " +
						buttonHover
					}
				>
					Logout
				</button>
			</div>
		</div>
	);
}