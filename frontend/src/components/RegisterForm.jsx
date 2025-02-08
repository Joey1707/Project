import {
	registerUser,
	validateEmail,
	validatePassword,
} from "../utils/network_data";
import { ErrorAlert, WarningAlert } from "../utils/alert_templates";

// Hooks
import useInput from "../hooks/useInput";
import useVisibility from "../hooks/useVisibility";
import { useState } from "react";
import { useNavigate } from "react-router";

// components
import { buttonHover, inputStyle } from "../styles/reusableSyles";
import { FaRegEye, FaRegEyeSlash } from "react-icons/fa";

export default function RegisterForm() {
	// Navigation Hooks
	const navigate = useNavigate(); //Redirects the user
	// Input Hooks
	const [username, setUsername] = useInput("");
	const [email, setEmail] = useInput("");
	const [passwd, setPassword] = useInput("");
	const [confirmPassword, setConfirmPassword] = useInput("");
	// Visibility Button Hooks
	const [isVisiblePass, toggleVisiblePass] = useVisibility();
	const [isVisibleConf, toggleVisibleConf] = useVisibility();
	// State Hooks
	const [valPaswd, setValPasswd] = useState("");
	const [isRegistering, setIsRegistering] = useState(false);

	const onSubmitHandler = async (event) => {
		event.preventDefault();
		const { errorMessage, isValid } = validatePassword(passwd);
		const passSame = passwd === confirmPassword ? true : false;
		const isEmailValid = validateEmail(email);

		if (!passSame) {
			ErrorAlert(
				"Password Error",
				"Password dan konfirmasi password tidak sama"
			);
		} else if (!isValid) {
			setValPasswd(errorMessage);
		} else if (!isEmailValid) {
			ErrorAlert("Invalid Email", "Email yang anda gunakan tidak valid");
		} else {
			if (!isRegistering) {
				setIsRegistering(true);
				const userData = { username, email, passwd };
				console.log("Submitting data:", userData);
				setValPasswd("");
				const { error } = await registerUser(userData); //Refer to register page for function
				if (!error) {
					navigate("/login");
				}
				setIsRegistering(false);
			} else {
				WarningAlert(
					"Please Wait!",
					"Mohon tunggu sebentar, data anda sedang di cek server!"
				);
			}
		}
	};

	return (
		<form
			onSubmit={onSubmitHandler}
			className="flex flex-col justify-between p-4 w-full h-full"
		>
			<div className="flex flex-col h-full w-full justify-center gap-1">
				<label
					htmlFor="usernameRegister"
					className="font-bold md:text-2xl text-lg"
				>
					Username:{" "}
				</label>
				<input
					id="usernameRegister"
					type="text"
					value={username}
					placeholder="username"
					onChange={setUsername}
					required
					className={inputStyle}
				/>
				<label htmlFor="emailRegister" className="font-bold md:text-2xl text-lg">
					Email:{" "}
				</label>
				<input
					id="emailRegister"
					type="email"
					value={email}
					placeholder="email"
					onChange={setEmail}
					required
					className={inputStyle}
				/>
				<label
					htmlFor="passwordRegister"
					className="font-bold md:text-2xl text-lg"
				>
					Password:{" "}
				</label>
				<div className="relative">
					<input
						id="passwordRegister"
						type={isVisiblePass ? "text" : "password"}
						value={passwd}
						placeholder="password"
						onChange={setPassword}
						required
						className={inputStyle}
					/>
					<button
						type="button"
						className="absolute right-[2%] md:top-[30%] top-[24%] text-2xl cursor-pointer z-1"
						onClick={toggleVisiblePass}
					>
						{isVisiblePass ? <FaRegEye /> : <FaRegEyeSlash />}
					</button>
				</div>
				<p className="text-red-500">{valPaswd}</p>
				<label htmlFor="confirmPassword" className="font-bold md:text-2xl text-lg">
					Konfirmasi Password:{" "}
				</label>
				<div className="relative">
					<input
						id="confirmPassword"
						type={isVisibleConf ? "text" : "password"}
						value={confirmPassword}
						placeholder="konfirmasi password"
						onChange={setConfirmPassword}
						required
						className={inputStyle}
					/>
					<button
						type="button"
						className="absolute right-[2%] md:top-[30%] top-[24%] text-2xl cursor-pointer z-1"
						onClick={toggleVisibleConf}
					>
						{isVisibleConf ? <FaRegEye /> : <FaRegEyeSlash />}
					</button>
				</div>
			</div>
			<button
				type="submit"
				className={
					"font-bold border-4 rounded-md md:mt-6 mt-3 text-xl md:p-4 p-3 cursor-pointer " +
					buttonHover
				}
				disabled={isRegistering}
			>
				{isRegistering ? "Submitting..." : "Submit"}
			</button>
		</form>
	);
}
